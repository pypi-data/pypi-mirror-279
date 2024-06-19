//@ts-nocheck
import * as LZString from 'lz-string';
import {
  NotebookPanel,
  NotebookModel,
  StaticNotebook,
  Notebook,
  NotebookActions
} from '@jupyterlab/notebook';
import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  IRouter
} from '@jupyterlab/application';
import { DocumentRegistry, Context } from '@jupyterlab/docregistry';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { ServiceManager } from '@jupyterlab/services';
import { ILauncher } from '@jupyterlab/launcher';
import { UUID } from '@lumino/coreutils';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { IEditorServices } from '@jupyterlab/codeeditor';

import { INotebookTracker } from '@jupyterlab/notebook';
import { ToolbarButton } from '@jupyterlab/apputils';

console.log('notebook_to_url_ext is loaded!');
console.log('Notebook:', Notebook);
console.log('NotebookActions:', NotebookActions);
import { Clipboard } from '@jupyterlab/apputils';

console.log('notebook_ephem is loaded!');

let savedParams: URLSearchParams | null = null;

// Save the URL parameters on page load
function saveUrlParameters(): void {
  const urlParams = new URLSearchParams(window.location.hash.slice(1));
  savedParams = urlParams;
  console.log('Saved URL parameters:', savedParams.toString());
}

let urlParams = new URLSearchParams(window.location.search);
console.log('urlParams', urlParams);

// Decompress the saved URL parameter and load notebook content
function decompressSavedContent(): any | null {
  if (savedParams) {
    console.log('savedParams', savedParams.get('notebook'));
    const compressedContent = savedParams.get('notebook');
    if (compressedContent) {
      const decompressedContent =
        LZString.decompressFromEncodedURIComponent(compressedContent);
      const content = JSON.parse(decompressedContent);
      console.log('decompressedContent', content);
      return content;
    }
  }
  return null;
}

// Add a route to render the temporary notebook
function addTempNotebookRoute(
  app: JupyterFrontEnd,
  filebrowserFactory: IFileBrowserFactory,
  router: IRouter
): void {
  // If available, Add to the router
  if (router) {
    console.log('router', router);
    app.commands.addCommand('notebook:start-nav', {
      label: 'Open Temp Notebook from URL',
      execute: async args => {
        const { request } = args as IRouter.ILocation;
        console.log('in request', args, request);

        const url = new URL(`http://example.com${request}`);
        const params = url.searchParams;
        const displayName = params.get('tempNotebook');
        console.log('displayName', displayName);

        const chatAfterRoute = async () => {
          router.routed.disconnect(chatAfterRoute);
          const { request } = router.current;
          console.log('chat after', displayName);
          if (displayName == 1) {
            console.log('in request', request);
            await app.commands.execute('notebook:open-temp', {
              url: '/temp-notebook'
            });
          }
        };

        router.routed.connect(chatAfterRoute);
      }
    });

    // // Use a specific pattern and higher rank
    // router.register({
    //   command: 'notebook:start-nav',
    //   pattern: /\/temp-notebook/,
    //   rank: 100
    // });
    /*
    app.commands.addCommand('notebook:open-temp', {
      label: 'Open Temporary Notebook',
      execute: async args => {
        console.log('executing create new');
        const tempName = `temp-notebook-${UUID.uuid4()}`;

        // Utility function to create a new notebook.
        const createNew = async (
          cwd: string,
          kernelId: string,
          kernelName: string,
          notebookName:string
        ) => {
          const model = await app.commands.execute(
            'docmanager:new-untitled',
            {
              path: cwd,
              type: 'notebook'
            }
          );
          console.log('created model', model);
          if (model !== undefined) {
            const widget = (await app.commands.execute('docmanager:open', {
              path: model.path,

              factory: 'Notebook',
              kernel: { id: kernelId, name: kernelName }
            })) as unknown as IDocumentWidget;
            widget.isUntitled = true;

            

            widget.context.rename(notebookName + '.ipynb');

            console.log('widget', widget);
            return widget;
          }
        };

        const currentBrowser =
          filebrowserFactory?.tracker.currentWidget ??
          filebrowserFactory.defaultBrowser;
        const cwd =
          (args['cwd'] as string) || (currentBrowser?.model.path ?? '');
        const kernelId = (args['kernelId'] as string) || '';
        const kernelName = (args['kernelName'] as string) || 'python3';

        const model = await createNew(cwd, kernelId, kernelName,tempName);
        console.log(
          'created model',
          model,
          cwd,
          'kernel',
          kernelId,
          'kernelName',
          kernelName
        );

        // Route to the new notebook
        const notebookPath = model.context.path;
        console.log('notebookPath', tempName);
        router.navigate('lab/'+tempName, { hard: false, silent: false });
        console.log('navigated')

        const content = decompressSavedContent();
      }
    });

  }*/

    app.commands.addCommand('notebook:open-temp', {
      label: 'Open Temporary Notebook',
      execute: async args => {
        console.log('executing create new');
        // Utility function to create a new notebook.
        const createNew = async (
          cwd: string,
          kernelId: string,
          kernelName: string
        ) => {

          const model = await app.commands.execute('docmanager:new-untitled', {
            path: cwd,
            type: 'notebook'
          });

          console.log('created model', model);

          if (model !== undefined) {
            const widget = (await app.commands.execute('docmanager:open', {
              path: model.path,
              factory: 'Notebook',
              kernel: { id: kernelId, name: kernelName }
            })) as unknown as IDocumentWidget;

            widget.isUntitled = true;

            const tempId = `temp-notebook-${UUID.uuid4()}`;
            

            await widget.context.rename(tempId + '.ipynb');

            console.log('widget', widget,widget.context.path);

            // set content of widget 
            const content = decompressSavedContent();
            console.log('content',content)
            if (content) {
              // Load the content into the notebook model
              const notebookModel = widget.context.model as NotebookModel;
              console.log('model', notebookModel);
              notebookModel.fromJSON(content);
    
              // Save the notebook context to ensure the content is written to disk
              await widget.context.save();
              console.log('Notebook content saved.');
            }
            


            // After creating the notebook, update the URL with the notebook path
            updateUrlWithNotebookPath(widget.context.path);


            return widget;
          }
        };

        const currentBrowser =
          filebrowserFactory?.tracker.currentWidget ??
          filebrowserFactory.defaultBrowser;
        const cwd =
          (args['cwd'] as string) || (currentBrowser?.model.path ?? '');
        const kernelId = (args['kernelId'] as string) || '';
        const kernelName = (args['kernelName'] as string) || '';

        const model = await createNew(cwd, kernelId, kernelName);
        console.log(
          'created model',
          model,
          cwd,
          'kernel',
          kernelId,
          'kernelName',
          kernelName
        );
      }
    });

    // Function to update the URL with the notebook path
    function updateUrlWithNotebookPath(notebookPath: string) {
      const url = new URL(window.location.href);
    

     

      // Create the retro view URL with the notebook path
      const retroViewUrl = `/notebooks/${notebookPath}?${url.search}&${url.hash}`;
      console.log('retro',retroViewUrl)
      window.location.href = retroViewUrl;

    }
  }
}

// Add a custom launcher item
function addTempNotebookLauncher(
  app: JupyterFrontEnd,
  launcher: ILauncher,
  router: IRouter
): void {
  const command = 'launcher:create-temp-notebook';
  app.commands.addCommand(command, {
    label: 'Temp Notebook',
    caption: 'Create a new temporary notebook',
    execute: () => {
      console.log('Navigating to /lab/temp-notebook...');
      //router.navigate('/lab/temp-notebook', { hard: false, silent: false });
    }
  });

  launcher.add({
    command,
    category: 'Other'
  });
}

// Compress the notebook text, set as URL parameter, and copy to clipboard
function compressNotebookContent(notebookPanel: any) {
  console.log(
    'notebook panel',
    notebookPanel,
    notebookPanel.context.model.toJSON()
  );
  const notebookContent = JSON.stringify(notebookPanel.context.model.toJSON());
  const compressedContent =
    LZString.compressToEncodedURIComponent(notebookContent);

  // Create a URL object from the current location
  const url = new URL(window.location.href);

  // now change it to be the origin + '/notebooks/' + notebookPath

  // Remove the notebook name from the path
  // const pathSegments = url.pathname.split('/');
  // if (pathSegments[pathSegments.length - 1].endsWith('.ipynb')) {
  //   console.log('found path', pathSegments[pathSegments.length - 1]);
  //   pathSegments.pop();
  // }

  
  const origin = url.origin;
  const route = '/lab/workspaces/auto-4/tree/'
  const nbpath = 'temp.ipynb'

  url.pathname = route + nbpath;

  //http://localhost:8888/lab/workspaces/auto-t/tree?tempNotebook=1#notebook=N4IgtgpgLghgJjWIBcoDWEBOA7CAbAZwAcIBjFUOAS2LxgE8B9bGSFEABXqgAsB7bAAIAzIIAUVIvQw58AShAAaEHWwBzAK4w1EdlN4ClIFm2Qh9-bMJABfZas3aIjKtgBmfCiFJ84EMFSYmHyYjGC+uqjGrJEgktyWRgBuWARUhsjCdiBuVHjOEAAeUBDYaRkgAHRSRgGQUPQk7CXFAPSFALQWhsomsd3YRtgARj7YKZhQjEVEISWYegk95vRqkNhQBIz5hVjs8QZWyanpg2bClQCMl5UADLbZIx6YYIhhriEoAKy9w8+vUBQABZlKR8IQUABtUBgvB4RgNJpmHx+IwEPgaTBg9j5KCCAC8X1q0HgiBgXigmA0BBKcBQlI0EGyRTIGigp0YPg0GxQl2UGKgRDZBChAF1lFQ6WYvsIvgA2UZwAAcHS+pAAnBAOkD1QAmYQdJWaoEdYTDADscEupD85uEMHIdhh4IRjViKN0ynRmOxZmJsAQSFQzN2pDZHK5POQ2A0cP5bKFmzFEqlIAQ6tuECVl11HVu6vVMG1wwgcA6w1ubku2rl6uEbnzMEut11ctsopsQA
 //http://localhost:8888/lab/temp.ipynb?tempNotebook=1#notebook=N4IgtgpgLghgJjWIBcoA2MB2BzArjbCAfQEtMAzAexVExkhRAAcBPKAC0sxABoQA3CACcAziS6MAzADoAjLOkAGXuBKQoLJhEZQIADygB6PQFpWHCXwDGlOBDAkhQykKJhb21CDoNkIEuac3HyCouLcyJIAvnys2JCYUCJEaPrCjAFsQZIqmABGNpihUET6TC66QoyBliDkJKmlBhCYYhJ+0qwgMSAA1sKYEGgiWlY03vSezFlcOXxwJCMYLEQ+UwAKM5gABJLbABSZ-UKDaACUKhg4+ITVW909+VRCYIhuZC4oAKx8Ty6vUBQABZrENhigANqgKxgogaLSMGx2FQiSi4IQwxj8GBCbYAXm2XxU6ngiBg4ygQlwIl0cBQlNwEB6aSsuCg4SINlwiRQsj4aKgTDZIkhAF0+CQ6X48gA2WQATnlQPlMBMinIACYgSYgTKIFYTPKvuQ4CYNYovnBFBqABwAdhtipl3R40Nh8KmSO0fFR6MxfmxQjNAB1guBoKSkF4GTSIFKGUy+Cy2RyuTzkBr+WyhUlIaBk+yuJy0enMyABTm4ZopgXiEIICJcGhAfMyRT9EYmBgyFIXeHYAgo8AolFxf4pSAbRBJHAgeR9SYvlYvoodeRJBrDXrtRAIDA7VYNXArPBJESYm60Ggqwi-F6UWiMVNiRHB+TUMy9PqU0W04DkJgTZoFmgrCmKEoTkCuowBAFqbpIMBWPKOo2pIkgmDAMoHmqFowjaeRAhAsg2uQ3SilEQA

  // Add the hash and query parameters
  url.hash = `notebook=${compressedContent}`;
  url.searchParams.set('tempNotebook', '1');

  const newUrl = url.toString();
  Clipboard.copyToSystem(newUrl);
  alert('URL copied to clipboard');
}

// Add "Save to URL" button to the notebook toolbar
function addSaveToUrlButton(
  app: JupyterFrontEnd,
  notebookTracker: INotebookTracker
) {
  const saveToUrlButton = new ToolbarButton({
    label: 'Save to URL',
    onClick: () => {
      const current = notebookTracker.currentWidget;
      if (current) {
        compressNotebookContent(current);
      }
    },
    tooltip: 'Save notebook content to URL and copy to clipboard'
  });

  notebookTracker.widgetAdded.connect((sender, panel) => {
    panel.toolbar.insertItem(10, 'saveToUrl', saveToUrlButton);
  });
}

import {
  IFileBrowserFactory,
  IDefaultFileBrowser
} from '@jupyterlab/filebrowser';

const extension: JupyterFrontEndPlugin<void> = {
  id: 'urlify-notebook',
  autoStart: true,
  requires: [IFileBrowserFactory, IRouter, ILauncher, INotebookTracker],
  activate: (
    app: JupyterFrontEnd,
    filebrowserFactory: IFileBrowserFactory,
    router: IRouter,
    launcher: ILauncher,
    notebookTracker: INotebookTracker
  ) => {
    // Use a specific pattern and higher rank
    // router.register({
    //   command: 'notebook:start-nav',
    //   pattern: /\/temp-notebook/,
    //   rank: 20
    // });
    // // Use a specific pattern and higher rank
    // router.register({
    //   command: 'notebook:start-nav',
    //   pattern: /.*/,
    //   rank: 20
    // });
    // Use a specific pattern and higher rank
    router.register({
      command: 'notebook:start-nav',
      pattern: /(tempNotebook=1)/,
      rank: 20
    });
    addSaveToUrlButton(app, notebookTracker);

    // Save the URL parameters when the app is first loaded
    saveUrlParameters();

    // Add the route to handle /lab/temp-notebook path
    addTempNotebookRoute(app, filebrowserFactory, router);

    // Add a custom launcher item
    addTempNotebookLauncher(app, launcher, router);
  }
};

export default extension;
