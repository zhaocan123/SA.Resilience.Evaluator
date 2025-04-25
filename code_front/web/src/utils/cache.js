class Cache {
    setCache(key, val){
        localStorage.setItem(key, JSON.stringify(val))
    }

    getCache(key){
        if(!localStorage.getItem(key)){
            return null
        }
        else{
            return JSON.parse(localStorage.getItem(key))
        }
    }

    removeCache(key){
        localStorage.removeItem(key)
    }
}

export default new Cache()
