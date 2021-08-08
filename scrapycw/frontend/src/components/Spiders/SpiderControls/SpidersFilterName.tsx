import { Search } from "@ui"
import { FC } from "react"
import styled from "styled-components"

interface SpidersFilterNameProps {
    onSearch: (text: string) => void
}

const StyledSearch = styled(Search)`
    width: 250px;
`

const SpidersFilterName: FC<SpidersFilterNameProps> = props => {
    return <StyledSearch placeholder="请输入爬虫名称!" onSearch={ props.onSearch } enterButton />
}

export { SpidersFilterNameProps }
export default SpidersFilterName