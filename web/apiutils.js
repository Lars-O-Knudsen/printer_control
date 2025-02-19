
class defaultHeaders {
    #hdrs={}
    constructor(headers=undefined){
        if (headers)
            Object.assign(this.#hdrs, headers);
    }

    get headers() {
        return this.#hdrs
    }

    add(header,value) {
        this.#hdrs[header] = value
    }
}

function apiError(operation,url,errorMsg, alertUser=true){
    msg = `An unexpected error occured during ${operation} on endpoint ${url}\nMessage was: ${errorMsg}`
    console.error(msg)
    if (alertUser) if(typeof process === 'object')
        alert(msg)
}

/*
** loads data from url and returns (success, data) or (failure, undefined) to supplied callback
*/
async function loadData(url, cb, opts={}, handleError=true) {
    fetch(url,opts)
        .then( resp => resp.json())
        .then( json => cb(true, json))
        .catch((error) => {
            if (handleError)
                apiError("fetch", url, error)
            cb(false, error)
        })
}
/*
** loads content/html from url and returns (success, data) or (failure, undefined) to supplied callback
*/
async function loadContent(url, cb, opts={}, handleError=true) {
    fetch(url,opts)
        .then((resp) => resp.text())
        .then((text) => cb(true, text))
        .catch((error) => {
            if (handleError)
                apiError("fetch", url, error)
            cb(false, error)
        })
}

function loadContentTo(url, id, opts={}) {
    loadContent(url, (ok, content) => {
            if (ok)  {
                document.getElementById(id).innerHTML = content
            }
        },
        opts
    )
}


function postData(url, data, cb, opts={},handleError=true) {
    base_opts={
        method: "POST",
        // mode: "same-origin", // no-cors, *cors, same-origin
        // cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        // credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json",
        },
        // redirect: "follow", // manual, *follow, error
        // referrerPolicy: "no-referrer",
        body: JSON.stringify(data),
    }
    base_opts=Object.assign(base_opts, opts)
    console.log(opts,base_opts)
    fetch(url, base_opts)
    .then( resp => resp.json())
    .then( json => cb(true, json))
    .catch((error) => {
        if (handleError)
            apiError("save", url, error)
        cb(false, error)
    })
}


function toISODateString(d) {
    return d.toISOString().substring(0,10)
}

function toISOTimeString(d, with100s=false) {
    return d.toISOString().substring(11, with100s ? 40 : 19)
}


// console.log(toISODateString(new Date()), toISOTimeString(new Date()), toISOTimeString(new Date(),true), new Date().toISOString())
// api_key="MmVRNXfxomie8fotBAFZyuR4ZBq7HrhIhlaL_2pVU3A"    
// hdrs={"Content-Type": "application/json","X-Api-Key":api_key}
// url="http://opi3b:5000/api/system/commands"
// reqInfo={
//     // method: "GET",
//     headers: hdrs
// }
// fetch(url,reqInfo)
// .then( resp => resp.json() )
// .then( json => console.log(json))
// .catch(error => console.error(error))
// loadData(url, (ok, content) => {console.log("----------------\n",ok,content)}, hdrs)
// loadContent(url, (ok, content) => {console.log("----------------\n",ok,content)}, hdrs)