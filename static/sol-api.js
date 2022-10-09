// load jquery 3.6.1
jquery = document.createElement("script")
jquery.src = 'https://code.jquery.com/jquery-3.6.1.min.js'
document.querySelector("head").appendChild(jquery)
delete jquery



const solAPI = {
    /**
     * 백엔드 API를 호출합니다
     * @param {string} api API 이름
     * @param {object=} data API 요청 본문
     * 
     * @returns {{ status:number, content:string }}
     */
    call_backend_api: function (api, data={}) {
        var res = $.ajax({
            url : "/api/" + api,
            method: "GET",
            data: data,
            async: false
        })
        console.log("[ solAPI - backend(" + api + ") ] ", {status: res.status, res: JSON.parse(res.responseText)})
        return {status: res.status, content: JSON.parse(res.responseText)}
    }
}

