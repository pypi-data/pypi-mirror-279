/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/


class PyodideSectionsRunner {

  no_undefined = prop =>{
      const getter = v => {
        if(v!==undefined) return v
        throw new Error(`Undefined is not allow: ${this.constructor.name}.${prop}.`)
      }
      return !(CONFIG._devMode && prop=='autoLogAssert') ? getter : v => getter(v==='null'?null:v)
      // Alternative getter needed for dev_docs...!
  }

  //JS_CONFIG_DUMP
  get attemptsLeft()      { return this.no_undefined('attemptsLeft')(this.data.attempts_left) }
  get autoLogAssert()     { return this.no_undefined('autoLogAssert')(this.data.auto_log_assert) }
  get corrRemsMask()      { return this.no_undefined('corrRemsMask')(this.data.corr_rems_mask) }
  get deactivateStdoutForSecrets(){ return this.no_undefined('deactivateStdoutForSecrets')(this.data.deactivate_stdout_for_secrets) }
  get decreaseAttemptsOnCodeError(){ return this.no_undefined('decreaseAttemptsOnCodeError')(this.data.decrease_attempts_on_code_error) }
  get envContent()        { return this.no_undefined('envContent')(this.data.env_content) }
  get envTermContent()    { return this.no_undefined('envTermContent')(this.data.env_term_content) }
  get excluded()          { return this.no_undefined('excluded')(this.data.excluded) }
  get excludedMethods()   { return this.no_undefined('excludedMethods')(this.data.excluded_methods) }
  get hasCheckBtn()       { return this.no_undefined('hasCheckBtn')(this.data.has_check_btn) }
  get isEncrypted()       { return this.no_undefined('isEncrypted')(this.data.is_encrypted) }
  get isVert()            { return this.no_undefined('isVert')(this.data.is_vert) }
  get maxIdeLines()       { return this.no_undefined('maxIdeLines')(this.data.max_ide_lines) }
  get postContent()       { return this.no_undefined('postContent')(this.data.post_content) }
  get postTermContent()   { return this.no_undefined('postTermContent')(this.data.post_term_content) }
  get prefillTerm()       { return this.no_undefined('prefillTerm')(this.data.prefill_term) }
  get publicTests()       { return this.no_undefined('publicTests')(this.data.public_tests) }
  get pyName()            { return this.no_undefined('pyName')(this.data.py_name) }
  get pythonLibs()        { return this.no_undefined('pythonLibs')(this.data.python_libs) }
  get recLimit()          { return this.no_undefined('recLimit')(this.data.rec_limit) }
  get secretTests()       { return this.no_undefined('secretTests')(this.data.secret_tests) }
  get showOnlyAssertionErrorsForSecrets(){ return this.no_undefined('showOnlyAssertionErrorsForSecrets')(this.data.show_only_assertion_errors_for_secrets) }
  get stdoutCutOff()      { return this.no_undefined('stdoutCutOff')(this.data.stdout_cut_off) }
  get userContent()       { return this.no_undefined('userContent')(this.data.user_content) }
  get whiteList()         { return this.no_undefined('whiteList')(this.data.white_list) }
  //JS_CONFIG_DUMP


  constructor(id){
    this.id = id
    this.decompressPagesIfNeeded()
    this.data = PAGE_IDES_CONFIG[id]
    if(CONFIG._devMode)
      CONFIG.objs[this.id] = this
    else{
      delete PAGE_IDES_CONFIG[id]
    }
    this.data.python_libs = new Set(this.data.python_libs)
    this.alreadyRanEnv = false
  }


  decompressPagesIfNeeded(){
    if(typeof(PAGE_IDES_CONFIG)!='string') return;
    const decompressed = decompressLZW(PAGE_IDES_CONFIG, "build.encrypted_js_data")
    PAGE_IDES_CONFIG = JSON.parse(
      decompressed, (key,val)=>key=='attempts_left' && val=="Infinity" ? Infinity : val
    )
  }


  build(){}   // For inheritance consistency


  /**Actions to perform when the current code in the editor has been extracted,
   * before anything is run.
   * */
  getCurrentEditorCode(){ return ""}


  /**Store code or command in the python runtime.
   * */
  storeUserCodeInPython(varName, code){
    // The double quotes are all escaped to make sure no multiline string will cause troubles
    const escapedCode = code.replace(/"/g, '\\"')
    pyodide.runPython(`__builtins__.${ varName } = """${ escapedCode }"""`)
  }

  globalTearDown(){}



  /**Runners without any terminal won't ever give feedback, unless it's a critical error.
   * In that case, a window alert will be used, so that it doesn't go unnoticed
   *
   * @returns: the concatenation of stdout and stdErr (useful in some places...).
   * */
  giveFeedback(stdout, stdErr="", forEnv=false){
    if(forEnv && stdErr){
      // Format back any escaped square brackets, because window.alert is not in the DOM...
      const msg = unEscapeSqBrackets(stdErr)
      window.alert(msg)
    }
    return stdout + stdErr
  }





  /**Given an editorName, automatically build the default options to pass as argument to the
   * runPythonCodeWithOptionsIfNoStdErr function.
   *
   * The content of the config optional argument will override any basic option, except for
   * the packagesAliases object, where the config.packagesAliases entries will be added.
   *
   * @returns: an options object, described as follow:
   *     @options :
   *          .autoLogAssert:   (boolean) If true, will automatically add the code of a failing
   *                            assertion as its message if it doesn't have one already.
   *          .excluded:        (String[]) Instructions to exclude at runtime.
   *          .excludedMethods: (String[]) Methods calls to exclude at runtime (string containment).
   *          .isPublic:        (boolean) Define if the executions are for public or secret tests.
   *          .packagesAliases: (Record<string,string>) mapping of imports that should be aliased
   *                            automatically for the user, if they try to import them.
   *          .recLimit:        (number) recursion depth (or -1 if not used)
   *          .runCodeAsync:    async python code runner.
   *          .withStdOut:      (boolean) Display the content of the stdOut or not.
   *          .whiteList:       (Array of strings) list of modules to import before the code
   *                            restrictions are put in place for the user's code.
   *
   * WARNING: If the editorName argument isn't given or is falsy, the fields excluded, whiteList
   *          and recLimit are not included.
   * */
  buildRunConfig(){
    return {
      // --- Python logistic related ---
      autoLogAssert:   true,            // default for the PUBLIC tests...
      excluded:        this.excluded,
      excludedMethods: this.excludedMethods,
      isPublic:        true,
      recLimit:        this.recLimit,
      runCodeAsync:    async (code) => pyodide.runPython(code),
      whiteList:       this.whiteList,
      withStdOut:      true,            // default for the PUBLIC tests...
      packagesAliases: {                // useless so far...
        // turtle: "pyo_js_turtle",     // this never got finished => unusable.
      },

      // --- Runtime logistic related ---
      stdErr: "",                       // First encountered error message
      finalMsg: CONFIG.lang.successMsg.msg,
      isAssertErr: false,               // is the error an assertion error
      envRuns: [],                      // keep track of the successfully run env sections (or raising assertion errors)
      userRunnable: true,               // Flag. If set to false, user code must not be run
      graphEnvRuns: {                   // Indicates runtime deps: the section as key is run only if:
        envTerm:  'env',                //    - the value is falsy
        postTerm: 'envTerm',            //    - the value is found in options.envRuns
        post:     'env',
      },
    }
  }





  /**Extract the content of an environment code, and run its content into pyodide environment.
   * Used for env, envTerm, postTerm and post.
   *
   * */
  async runEnvironmentAsync(options, name) {
    const runIf =   options.graphEnvRuns[name]
    const toRun   = !runIf || options.envRuns.includes(runIf)
    const content = name && this[`${ name }Content`].trim()

    if(!toRun) return

    let ranSection = false
    let localErr   = ""
    setupStdIO()    // ALWAYS! (see finally)

    try{
      if(content){
        // make sure packages are installed, then run code content:
        await this.installAndImportMissingModules(content, options, true)
        await pyodide.runPythonAsync(content, {filename: `<${ toSnake(name) }>`})
      }
      ranSection = true

      }catch(err){
          // If an error occurred, give feedback in the console, with stdout teardown on the way,
          // then stop everything :
          options.userRunnable = false
          ;[options.stdErr, options.isAssertErr] = generateErrorLog(err)
          localErr = options.stdErr  // use local var to make sure no weird global interactions.
          if(options.isAssertErr && name.startsWith('env')){
            ranSection=true
          }
      }finally{
        this.giveFeedback(getFullStdIO(), localErr, true)
        if(ranSection) options.envRuns.push(name)
      }
    }





  /**Explore the user's code to find missing modules to install. If some are found, load
   * micropip (if not done yet), then install all the missing modules.
   * Also import all the packages present in options.whiteList.
   *
   * NOTE: python libs are identified peeking into the global config, but are actually
   * loaded only if they are available in the instance property (this is to limit the
   * _SAVAGE_ unexpected installations of random packages from PyPI).
   *
   * @code : the python code to run.
   * @options :Same as `buildRunConfig`.
   * */
  async installAndImportMissingModules(code, options, isFromsEnv=false){

    const installedModules = getAvailablePackages()
    const neededModules = getUserImportedModules(code).filter(
      name => !installedModules.has(name) && (isFromsEnv || !options.excluded.includes(name))
    )

    // Using this.pythonLibs because only the available ones can be downloaded
    const pyLibsMissing = neededModules.filter( name => this.pythonLibs.has(name) )

    // Using CONFIG.pythonLibs so that an unavailable custom lib doesn't trigger a
    // "savage install" from PyPI.
    const externalsMissing = neededModules.filter( name => !CONFIG.pythonLibs.has(name) )

    const pkgReplacements = options.packagesAliases
    const whiteList = options.whiteList.filter(name=>!installedModules.has(name))
    externalsMissing.push(...whiteList)


    /*
    Things to import whatever happens: thing are complicated, here...

    * Installing packages via micropip doesn't actually import them in the environment. It works
      the same for custom python libs.
    * PMT needs to know up front what packages are missing or not, to decide when to display the
    installation messages or not.
    * installed packages can be found through micropip, but not _loaded_ custom packages.
    * So, spotting missing packages relies on picking in sys.modules, BUT they actually end up
      there _ONLY_ if a python code actually imported them, going through `import xxx`.

    So far, so good. Problems arise with additional features:
    * White lists: their content has to be actually imported in the global scope (if ever used...)
    * Custom libs have to be actually imported so that they are visible on the next import attempt...
    * ...which may occur right after that because of commands in terminals (env+env_term)
    * Exclusions:
        - they are not applied on env sections, so modules _may_ be loaded there
        - so they _have_ to be actually imported...
        - but hidden inside a function, so that they do not leak in the global scope...
    */

    const preImport = whiteList.map(name=>'import '+name)
    const hiddenImport=[]

    const importLater=(name, import_as='')=>{
      const arr = options.excluded.includes(name) ? hiddenImport : preImport
      arr.push( import_as || 'import '+name )
    }

    if(externalsMissing.length || pyLibsMissing.length){
      this.giveFeedback(CONFIG.lang.installStart.msg)

      for(const lib of pyLibsMissing){
        const archive = `${ CONFIG.baseUrl }/${ lib }.zip`
        const zipResponse = await fetch(archive)
        const zipBinary   = await zipResponse.arrayBuffer()
        pyodide.unpackArchive(zipBinary, "zip", {extractDir: lib})
        importLater(lib)
      }

      if(externalsMissing.length){
        await pyodide.loadPackage("micropip");
        let micropip = pyodide.pyimport("micropip");

        for(let lib of externalsMissing){
          if(lib in pkgReplacements){
            importLater(lib, `import ${ pkgReplacements[lib] } as ${ lib }`)
            lib = pkgReplacements[lib]
          }
          jsLogger("[Micropip] - Install", lib)
          await micropip.install(lib);
          importLater(lib)
        }
      }

      this.giveFeedback(CONFIG.lang.installDone.msg)
    }

    // Import everything that is needed (either because module aliasing or because the code
    // restrictions would forbid it later):
    if(preImport.length){
      pyodide.runPython(preImport.join('\n'))
    }
    if(hiddenImport.length){
      const imports = `def _hack_imports():\n    ${ hiddenImport.join('\n    ') }\n_hack_imports() ; del _hack_imports`
      pyodide.runPython(imports)
    }
  }






  /** 1. Refresh the features defined in pyodide environment, in case the user messed with them
   *     (accidentally or not).
   *  2. Then run the content of the `env` section.
   *
   * @returns: [options, isOk].
   *     If isOk is false, an error has been raised: this is a CRITICAL ERROR and executions at
   *     upper level must be stopped.
   * */
  async setupRuntime(){

    Object.entries({
      exclusionsTools: true,
      inputPrompt: true,
      version: true,
      refresher: true,
      upDownLoader: true,
    }).forEach( ([opt,todo]) => {
        jsLogger("[Feature (re-/load)] -", opt)
        if(todo) pyodide.runPython(terminalFeatureCode(opt))
    })

    // Build the default configuration options to use to run the user's code:
    const options = this.buildRunConfig()
    await this.runEnvironmentAsync(options, 'env')
    this.alreadyRanEnv = true
    return options
  }



/**Takes a code as argument, and run it in the pyodide environment, using various options:
 *
 * @throws: Any JS runtime Error, if something went very wrong... (python errors are swallowed
 *          and just printed to the terminal)
 * @returns: The stdErr formatted string message that got printed in the terminal, or empty
 *           string if no error.
 *           Note that the message is displayed in the console already, so this is only a
 *           "marker" to propagate some logic in other parts of the application.
 *
 * NOTE:
 *    - Pyodide itself is using eval, so replacing globally the builtin will cause a lot of
 *      troubles and just won't work.
 *    - This function doesn't take in charge the pyodide environment setup, (preparation,
 *      rebuilding the setup, ...).
 *    - On the other hand it DOES take in charge installation of missing modules/packages
 *      in the user's/given code.
 */
async runPythonCodeWithOptionsIfNoStdErr(code, options){

    // Do nothing if nothing to do...!
    if(options.stdErr || !code.trim()) return;

    try{
      // Do first the methods exclusions check, to gain some time (avoids loading modules if
      // the error would show up anyway after loading them)
      const nope = options.excludedMethods.filter(methodCall=>code.includes(methodCall))
      if(nope.length){
        const plural = nope.length>1 ? "s":""
        const nopes = nope.map( s=>s.slice(1) ).join(', ')
        const msg = `${ CONFIG.MSG.exclusionMarker } method${plural}: ${ nopes }`
        throw new PythonError(msg)
      }

      // Detect possible user imports and install the packages to allow their imports:
      await this.installAndImportMissingModules(code, options)

    }catch(err){
      ;[options.stdErr,] = generateErrorLog(err, code, false, !options.isPublic)
      this.giveFeedback("", options.stdErr)
      return
    }

    const withExclusions = options.excluded.length>0 || options.recLimit > 0

    // Setup stdout capture. WARNING: this must always be done even if it's not shown to the user.
    // If not done, a previous execution might have close the StringIO and if ever the user prints
    // something, it would result in an error without that:
    setupStdIO()

    // Setup code/imports exclusions if any (later id better)
    if(withExclusions) setupExclusions(options.excluded, options.recLimit)

    let stdOut="", delayedErr, _   // "_" to avoid loosing lodash...
    try {
      await options.runCodeAsync(code)
    }catch(err){
      // Since generateErrorLog might run python code, the exclusions must be removed _before_
      // the function is called, so store the error for later use.
      delayedErr = err

    } finally {
      // Teardown steps must always occur, whatever happened (even for JS errors), hence in a
      // finally close, and they also must be protected against failure, so in their own
      // try/catch/finally construct:
      try {
        if(withExclusions) restoreOriginalFunctions(options.excluded)

        // Now only, compute the error message if needed.
        if(delayedErr){
            ;[options.stdErr, _] = generateErrorLog(delayedErr, code, options.autoLogAssert, !options.isPublic)
        }

        // Always extract the stdout and close the buffer (avoid memory leaks)
        let captured = getFullStdIO()

        // Send stdout feedback to the user only if allowed:
        if(options.withStdOut){
          stdOut = textShortener(captured)
        }

      }catch(err){
        // This second catch is there so that the user can see the JS error in the terminal.
        // (Note: maybe I should actually throw them again...?)
        ;[options.stdErr, _] = generateErrorLog(err, code, true)

      } finally {
        // Use a finally clause, in case something went wrong in generateErrorLog...
        // (the message probably won't be accurate, but at least, something will be visible)
        this.giveFeedback(stdOut, options.stdErr)
      }
    }
  }




  async teardownRuntime(options){
    jsLogger("[Teardown] - PyodideRunner")
    await this.runEnvironmentAsync(options, 'post')
    this.globalTearDown()
  }
}
