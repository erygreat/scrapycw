import srequest from "./srequest"

type Spiders = Array<{
    project: string,
    spiders: Array<string>,
}>

export default {
    spiders: async () => {
        return await srequest.get<Spiders>({ url: "/i/spiders" })
    }
}