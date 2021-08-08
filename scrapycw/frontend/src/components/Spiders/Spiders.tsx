import interfaces from "@/interfaces";
import { message } from "@ui";
import { useCallback, useEffect, useRef, useState } from "react";
import styled from "styled-components";
import { SpidersData } from "./types.d";
import SpidersControls from "./SpiderControls";
import SpidersTable from "./SpidersTable";

const StyledSpiders = styled.div`
    padding: 0 40px;
    height: 100%;
    display: flex;
    align-items: stretch;
    flex-direction: column;
`

const Spiders = () => {

    const [loading, setLoading] = useState<boolean>(false);
    const [spiders, setSpiders] = useState<SpidersData>([]);
    const [projects, setProjects] = useState<Array<string>>([]);
    const originSpidersRef = useRef<SpidersData>([]);
    const filterNameRef = useRef<string>("");
    const filterProjectRef = useRef<string>("");

    const getSpiders = useCallback(async () => {
        setLoading(true);
        const response = await interfaces.spiders();
        setLoading(false);
        if(response.success) {
            const _spiders = response.data;
            let results: SpidersData = [];
            let _projects: Array<string> = [];
            _spiders.forEach(item => {
                const project = item.project;
                if(!projects.includes(project)) {
                    _projects.push(project);
                }
                const children = item.spiders.map(spider => {
                    return {
                        project,
                        spider: spider,
                        key: project + "|" + spider
                    }
                });
                results = results.concat(children)
            })
            originSpidersRef.current = results;
            setProjects(_projects);
            handlerSpiders();
        } else {
            const messageText = response.message;
            const code = response.httpStatus;
            const status = response.serverStatus;
            message.error(`查询失败请刷新重试, 错误信息: [${ code || status }] ${ messageText }`)
        }
    }, [])

    useEffect(() => {
        getSpiders()
    }, [])

    const handlerSpiders = () => {
        const _spiders = originSpidersRef.current;
        const _filterName = filterNameRef.current;
        const _filterProject = filterProjectRef.current;
        const showSpiders = _spiders.filter(item => {
            if(_filterProject && item.project !== _filterProject) {
                return false;
            }
            return item.spider.indexOf(_filterName) >= 0;
        })
        setSpiders(showSpiders);
    }

    const handlerSearch = (text: string) => {
        filterNameRef.current = text;
        handlerSpiders();
    }

    const handlerChangeProject = (project: string) => {
        filterProjectRef.current = project;
        handlerSpiders();
    }

    return <StyledSpiders>
        <SpidersControls
            loading={ loading }
            onReload={ getSpiders }
            projects={ projects }
            onSearch={ handlerSearch }
            onChangeProject={ handlerChangeProject }
        />
        <SpidersTable spiders={ spiders } loading={ loading }></SpidersTable>
    </StyledSpiders>
}

export default Spiders;