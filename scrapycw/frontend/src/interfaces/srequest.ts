import ScrapycwException from "@/utils/exception";
import axios, { AxiosResponse } from "axios";

interface ResponseInterface<T> {
    success: boolean,
    message: string,
    code: number
    data: T
}

export interface Response<T> extends ResponseInterface<T> {
    success: true,
}

export interface URLParam {
    [key: string]: string | number
}

export interface RequestOptions<Req> {
    url: string,
    params?: URLSearchParams,
    data?: Req,
    method?: "post" | "get"
}

export const DEFAULT_HTTP_RESPONSE_CODE = 0;
export const DEFAULT_SERVER_RESPONSE_CODE = 0;

export interface ScrapycwRequestExceptionInterface {
    success: false
    message: string
    httpStatus: number
    serverStatus: number
    error?: Error
}

export class ScrapycwRequestException extends ScrapycwException implements ScrapycwRequestExceptionInterface {

    public readonly success = false;

    constructor(
        public readonly message: string,
        public readonly httpStatus: number = DEFAULT_HTTP_RESPONSE_CODE,
        public readonly serverStatus: number = DEFAULT_SERVER_RESPONSE_CODE,
        public readonly error?: Error
    ) {
        super();
    }
}

const getUrl = (url: string, params?: URLSearchParams): string => {
    const urlObj = new URL(window.location.href);
    urlObj.pathname = url
    urlObj.search = new URLSearchParams(params).toString();
    return urlObj.toString();
}

const request = async <Res, Req = null>(options: RequestOptions<Req>): Promise<Response<Res> | ScrapycwRequestException> => {
    const originUrl = options.url;
    const params = options.params;
    const data = options.data;
    const url = getUrl(originUrl, params);
    try {
        const res: AxiosResponse<ResponseInterface<Res>> = await axios(url, { data: data, method: options.method || 'get' })
        const response = res.data;
        if(response.success) {
            return response as Response<Res>
        } else {
            return new ScrapycwRequestException(response.message || '', res.status, response.code)
        }
    } catch(error) {
        let response: AxiosResponse = error.response;
        if (response) {
            return new ScrapycwRequestException(response.statusText, response.status, error=error)
        } else {
            return new ScrapycwRequestException(error.message, error=error)
        }
    }
}

const get = async <Res, Req = null>(options: RequestOptions<Req>): Promise<Response<Res> | ScrapycwRequestException> => {
    options.method = "get";
    return await request(options);
}

const post = async <Res, Req = null>(options: RequestOptions<Req>): Promise<Response<Res> | ScrapycwRequestException> => {
    options.method = "post";
    return await request(options);
}

export default {
    request,
    get,
    post,
}