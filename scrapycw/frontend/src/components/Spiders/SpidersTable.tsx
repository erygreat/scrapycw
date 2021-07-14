import interfaces from "@/interfaces";
import { Message, Table } from "@/ui";
import { useCallback, useEffect, useState } from "react";
import styled from "styled-components";

interface SpiderTableData {
    spider: string
    project: string
    key: string
}

const StyledSpiders = styled.div`
    padding: 20px 40px;
`

const SpidersTable = () => {

    const [loading, setLoading] = useState<boolean>(false);
    const [spiders, setSpiders] = useState<Array<SpiderTableData>>([]);
    const columns = [
        { title: '项目', dataIndex: 'project', key: 'project'},
        { title: '名称', dataIndex: 'spider', key: 'spider'},
        { 
            title: "操作",
            key: 'options', 
            render: (text: SpiderTableData, record: SpiderTableData) => {
                return <div></div>
                // return <Options {...record}></Options>
            }
        }
    ]

    const requestSpiders = useCallback(async () => {
        setLoading(true);
        const response = await interfaces.spiders();
        setLoading(false);
        if(response.success) {
            const _spiders = response.data;
            let results: Array<SpiderTableData> = [];
            _spiders.forEach(item => {
                const project = item.project;
                const children = item.spiders.map(spider => {
                    return {
                        project,
                        spider: spider,
                        key: project + "|" + spider
                    }
                });
                results = results.concat(children)
            })
            setSpiders(results);
        } else {
            const message = response.message;
            const code = response.httpStatus;
            const status = response.serverStatus;
            Message.error(`查询失败请刷新重试, 错误信息: [${ code || status }] ${ message }`)
        }
    }, [])

    useEffect(() => {
        requestSpiders()
    }, [])

    return <StyledSpiders>
        <Table dataSource={ spiders } columns={ columns } pagination={{ hideOnSinglePage: true }} loading={ loading } bordered></Table>
    </StyledSpiders>
}

export default SpidersTable;