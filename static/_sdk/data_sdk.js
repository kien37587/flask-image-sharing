(function(){
  // Minimal data SDK that proxies to backend API /api/images
  window.dataSdk = {
    async init(handler){
      this._handler = handler || {};
      // fetch existing images with timeout
      try{
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), 15000);
        const res = await fetch('/api/images', {signal: controller.signal});
        clearTimeout(id);
        if(!res.ok) {
          const text = await res.text().catch(()=>'');
          throw new Error(`HTTP ${res.status} ${text}`);
        }
        const data = await res.json();
        if(this._handler && typeof this._handler.onDataChanged === 'function'){
          this._handler.onDataChanged(data);
        }
        return {isOk:true, data};
      }catch(e){
        console.error('dataSdk init error', e);
        return {isOk:false, error:String(e)};
      }
    },
    async create(obj){
      // Add timeout and better error reporting
      try{
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), 15000);
        const res = await fetch('/api/images', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify(obj),
          signal: controller.signal
        });
        clearTimeout(id);
        if(!res.ok){
          const text = await res.text().catch(()=>'');
          return {isOk:false, error:`HTTP ${res.status} ${text}`};
        }
        const data = await res.json();
        if(data.isOk){
          // refresh (with timeout)
          const ctrl2 = new AbortController();
          const id2 = setTimeout(()=>ctrl2.abort(),15000);
          const listRes = await fetch('/api/images',{signal:ctrl2.signal});
          clearTimeout(id2);
          const list = listRes.ok ? await listRes.json() : [];
          if(this._handler && typeof this._handler.onDataChanged === 'function'){
            this._handler.onDataChanged(list);
          }
        }
        return data;
      }catch(e){
        console.error('dataSdk.create error', e);
        return {isOk:false, error:String(e)};
      }
    },
    async delete(obj){
      try{
        const id = obj.id || obj;
        const controller = new AbortController();
        const tid = setTimeout(()=>controller.abort(),15000);
        const res = await fetch('/api/images/'+encodeURIComponent(id), {method:'DELETE', signal:controller.signal});
        clearTimeout(tid);
        if(!res.ok){
          const text = await res.text().catch(()=>'');
          return {isOk:false, error:`HTTP ${res.status} ${text}`};
        }
        const data = await res.json();
        if(data.isOk){
          const ctrl2 = new AbortController();
          const id2 = setTimeout(()=>ctrl2.abort(),15000);
          const listRes = await fetch('/api/images',{signal:ctrl2.signal});
          clearTimeout(id2);
          const list = listRes.ok ? await listRes.json() : [];
          if(this._handler && typeof this._handler.onDataChanged === 'function'){
            this._handler.onDataChanged(list);
          }
        }
        return data;
      }catch(e){
        console.error('dataSdk.delete error', e);
        return {isOk:false, error:String(e)};
      }
    }
  };
})();
