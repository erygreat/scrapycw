import React, {FC, useEffect, useState} from 'react';
import { Table, message } from '@/components/ui';
import { Options } from "./options";
import { DataSpider } from './types'
import style from './spider.module.css';
import { getAllSpiders } from "@/utils/scrapycw";

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
                return <Options {...record}></Options>
            }
        }
    ]
    useEffect(() => {
        getAllSpiders({
            onSuccess(response) {
                let _spiders = [];
                let data = response.data;
                for(let projectObj of data) {
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
                setLoading(false);
            },
            onError(msg) {
                message.error("查询错误，请刷新重试, 错误信息：【" + msg + "】");
                setLoading(false);
            }
        })
    }, [])

    return <div className={style.spider}>
        <Table dataSource={spiders} columns={columns} pagination={{ hideOnSinglePage: true }} loading={loading} bordered></Table>
    </div>
}
