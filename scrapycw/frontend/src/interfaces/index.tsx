import srequest from "@/utils/srequest"

type Spiders = Array<{
    project: string,
    spiders: Array<string>,
}>

export default {
    spiders: async () => {
        return await srequest.get<Spiders>({ url: "/i/spiders" })
    },
    runSpider: async (data: any) => {
        return await srequest.post({ url: "/i/crawl", data})
    }
}