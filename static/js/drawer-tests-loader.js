/**
 * Drawer Tests Loader
 * Dynamically populates all files from tests and sujets0 lists consecutively in the right drawer
 */

document.addEventListener('DOMContentLoaded', function() {
  const backendSettings = document.getElementById('backend-public-settings');
  const allFilesList = document.getElementById('doppel-all-files-list');
  
  if (backendSettings && allFilesList) {
    // Combine all files from both sources
    const allFiles = [];
    
    // Get tests files
    const testsData = backendSettings.dataset.doppel_tests_script_name_list;
    if (testsData) {
      try {
        const testsFiles = JSON.parse(testsData);
        allFiles.push(...testsFiles.filter(file => 
          file.endsWith('.py') && 
          !file.startsWith('__') && 
          file !== '__pycache__' &&
          file !== 'corrector.py' && 
          file !== 'defaults.py'
        ));
      } catch (error) {
        console.error('Error parsing DOPPEL_TESTS_SCRIPT_NAME_LIST:', error);
      }
    }
    
    // Get sujets0 files
    const sujets0Data = backendSettings.dataset.doppel_sujets0_script_name_list;
    if (sujets0Data) {
      try {
        const sujets0Files = JSON.parse(sujets0Data);
        allFiles.push(...sujets0Files.filter(file => 
          file.endsWith('.py') && 
          !file.startsWith('__') && 
          file !== '__pycache__' &&
          file !== 'corrector.py' && 
          file !== 'defaults.py'
        ));
      } catch (error) {
        console.error('Error parsing DOPPEL_SUJETS0_SCRIPT_NAME_LIST:', error);
      }
    }
    
    // Sort all files alphabetically
    allFiles.sort();
    
    // Create list items for all files
    allFiles.forEach(function(scriptName) {
      const li = document.createElement('li');
      // Note: Using hardcoded URL in JS is consistent with other files like consistent-executor.js
      li.innerHTML = `
        <a href="/doppel/execute-back-and-front/${encodeURIComponent(scriptName)}" 
           class="hover:bg-primary hover:text-primary-content text-sm"
           title="Execute ${scriptName} in both backend and frontend">
          <svg xmlns="http://www.w3.org/2000/svg"
               fill="none"
               viewBox="0 0 24 24"
               stroke-width="1.5"
               stroke="currentColor"
               class="h-3 w-3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
          <span class="flex-1">${scriptName.substring(0, 21)}</span>
          <svg xmlns="http://www.w3.org/2000/svg"
               fill="none"
               viewBox="0 0 24 24"
               stroke-width="1.5"
               stroke="currentColor"
               class="h-3 w-3 opacity-50">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </a>
      `;
      allFilesList.appendChild(li);
    });
  }
}); 