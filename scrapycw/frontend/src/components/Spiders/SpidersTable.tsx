import { Table } from "@ui";
import { FC, useEffect, useRef } from "react";
import { SpiderData, SpidersData } from "./types.d";
import Options from "./SpiderOptions";
import styled from "styled-components";

interface SpidersTableProps {
    loading: boolean
    spiders: SpidersData
}

const StyledTable = styled.div`
    flex: auto;
    padding-bottom: 10px;
    overflow: hidden;
    .ant-table-container {
        height: 100%;
        display: flex;
        flex-direction: column;
    }
`

const SpidersTable: FC<SpidersTableProps> = props => {

    const tableRef = useRef<HTMLDivElement>(null);

    const columns = [
        { title: '项目', dataIndex: 'project', key: 'project'},
        { title: '名称', dataIndex: 'spider', key: 'spider'},
        { 
            title: "操作",
            key: 'options', 
            render: (text: SpiderData, record: SpiderData) => {
                return <Options spider={ record }></Options>
            }
        }
    ]

    useEffect(() => {
        if (tableRef.current) {
            tableRef.current.style.height = tableRef.current.scrollHeight + "px"
        }
    }, [])

    return <StyledTable ref={ tableRef }>
        <Table scroll={{ y: 'auto'}} dataSource={ props.spiders } columns={ columns } pagination={ false } loading={ props.loading } bordered />
    </StyledTable>
}

export default SpidersTable;