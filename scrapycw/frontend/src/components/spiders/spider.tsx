import React, {FC, useEffect, useState} from 'react';
import { Table } from '@/components/ui';
import axios from 'axios';
import { SpiderOptions } from "./spider-options";
import { DataSpider, QueryAllSpiderResponse } from './types'
import style from './index.module.css';

export const Spider: FC = () => {
    const [spiders, setSpiders] = useState<Array<DataSpider>>([]);
    const [loading, setLoading] = useState(true);
    const columns = [
        { title: '所属项目', dataIndex: 'project', key: 'project'},
        { title: '名称', dataIndex: 'spider', key: 'spider'},
        { 
            title: "操作",
            key: 'options', 
            render: (text: DataSpider, record: DataSpider) => {
                return <SpiderOptions {...record}></SpiderOptions>
            }
        }
    ]
    useEffect(() => {
        axios.get("/i/all-spiders").then((response: {data: QueryAllSpiderResponse}) => {
            const result = response.data;
            if(result.success) {
                const projectObjs = result.data;
                let _spiders = [];
                for(let projectObj of projectObjs) {
                    let project = projectObj.project;
                    for(let spider of projectObj.spiders) {
                        _spiders.push({
                            project: project,
                            spider: spider,
                            key: project.toString() + spider.toString()
                        })
                    }
                }
                setSpiders(_spiders);
            } else {
                console.warn("查询失败:", result);
                alert(result.message);
            }
            setLoading(false);
        }).catch((error): void => {
            console.error(error);
            alert("服务器错误, 请刷新重试! ");
            setLoading(false);
        })
    }, [])

    return <div className={style.spider}>
        <Table dataSource={spiders} columns={columns} pagination={{ hideOnSinglePage: true }} loading={loading} bordered></Table>
    </div>
}
