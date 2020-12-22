import axios from 'axios';
import { AxiosResponse } from 'axios'
import { URLParam, RequestOptions, RunSpiderOptions, Response, QueryAllSpiderOptions } from "./types";


const DEFAULT_HTTP_ERROR_CODE = -1;
const DEFAULT_SERVER_ERROR_CODE = -1;

const getUrl = (url: string, params: URLParam | null | undefined): string => {
    let urlParam = '';
    if(params) {
        for(let key in params) {
            let value = params[key] || '';
            urlParam += '&' + encodeURIComponent(key) + "=" + encodeURIComponent(value); 
        }
    }
    if(url.indexOf('?') < 0 && urlParam) {
        return url + '?' + urlParam.substring(1);
    } else if(urlParam) {
        return url + urlParam;
    } else {
        return url;
    }
}


const request = <T extends Response<U>, U>(options: RequestOptions<T>) => {
    let url = options.url;
    let params = options.params;
    let data = options.data;
    url = getUrl(url, params);
    axios({
        url: url,
        data: data,
        method: options.method || 'get'
    }).then((e: AxiosResponse<T>) => {
        let response = e.data;
        let isSuccess = response.success;
        if(isSuccess && options.onSuccess) {
            options.onSuccess(response);
        } else if(!isSuccess && options.onError) {
            options.onError(response.message || '', e.status, response.code);
        }
    }).catch(error => {
        if(!options.onError) {
            return;
        }
        let response: AxiosResponse = error.response as AxiosResponse;
        if (response) {
            options.onError(response.statusText, response.status, DEFAULT_SERVER_ERROR_CODE, error);
        } else if(error.request){
            options.onError(error.message, DEFAULT_HTTP_ERROR_CODE, DEFAULT_SERVER_ERROR_CODE, error);
        }
    })
}

const get = <T extends Response<U>, U>(options: RequestOptions<T>) => {
    options.method = "get";
    request(options);
}

const post = <T extends Response<U>, U>(options: RequestOptions<T>) => {
    options.method = "post";
    request(options);
}

export const runSpider = (options: RunSpiderOptions) => {
    post({
        url: "/i/crawl",
        params: {
            spider: options.spider,
            project: options.project
        },
        data: {
            spargs: options.spargs,
            settings: options.settings
        },
        onSuccess: options.onSuccess,
        onError: options.onError,
    });
}

export const getAllSpiders = (options: QueryAllSpiderOptions) => {
    get({
        url: "/i/all-spiders",
        onSuccess: options.onSuccess,
        onError: options.onError
    })
}