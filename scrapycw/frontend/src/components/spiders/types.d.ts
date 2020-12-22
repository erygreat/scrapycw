import { Response } from "@/components/types";

export interface QuerySpider {
    project: string,
    spiders: Array<string>,
}
export interface QueryAllSpiderResponse extends Response<Array<QuerySpider>> {}

export interface DataSpider {
    project: string,
    spider: string,
    key?: string,
}