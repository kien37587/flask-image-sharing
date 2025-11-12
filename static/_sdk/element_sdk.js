(function(){
  // Minimal element SDK that supports init and simple config management used by templates
  window.elementSdk = {
    _config: {},
    init(opts){
      opts = opts || {};
      this._opts = opts;
      // start with defaultConfig if provided
      this._config = opts.defaultConfig || {};
      // call onConfigChange if provided
      if(typeof opts.onConfigChange === 'function'){
        opts.onConfigChange(this._config);
      }
      return {isOk:true};
    },
    setConfig(partial){
      this._config = Object.assign({}, this._config, partial);
      if(this._opts && typeof this._opts.onConfigChange === 'function'){
        this._opts.onConfigChange(this._config);
      }
    },
    get config(){
      return this._config;
    }
  };
})();
