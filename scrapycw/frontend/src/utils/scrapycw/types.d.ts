export interface URLParam {
    [key: string]: string | number | null | undefined
}
export interface RequestOptions<T> {
    url: string,
    params?: URLParam | null | undefined,
    data?: any,
    method?: "post" | "get"
    onSuccess?: (response: T) => void,
    onError?: (message?: string, httpCode?: number, serverCode?: number, error?: Error) => void,
}
export interface Response<T> {
    code: number,
    data: T,
    message: string | null,
    success: boolean,
}

/** 运行爬虫 */
export interface RunSpiderResponseData {
    job_id: string,
}
export interface RunSpiderOptions {
    spider: string,
    project: string,
    settings?: {
        [propName: string]: any;
    } | null,
    spargs?: {
        [propName: string]: any;
    } | null,
    onSuccess?: (response: Response<RunSpiderResponseData>) => void,
    onError?: (message?: string, httpCode?: number, serverCode?: number, error?: Error) => void,
}


/** 查询所有爬虫 */
export interface QuerySpider {
    project: string,
    spiders: Array<string>,
}
export interface QueryAllSpiderResponse extends Response<Array<QuerySpider>> {}
export interface QueryAllSpiderOptions {
    onSuccess?: (response: QueryAllSpiderResponse) => void,
    onError?: (message?: string, httpCode?: number, serverCode?: number, error?: Error) => void,
}