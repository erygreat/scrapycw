import { Select } from "@ui"
import { FC } from "react"
import styled from "styled-components"

interface SpidersFilterProjectProps {
    onChangeProject: (project: string) => void
    projects: Array<string>
}

const Option = Select.Option;

const StyledSelectForm = styled.div`
    margin-left: 10px;
`
const StyledSelect = styled(Select)`
    margin-left: 5px;
    width: 100px;
`

const SpidersFilterProject: FC<SpidersFilterProjectProps> = props => {
    return <StyledSelectForm>
        项目名称:
        <StyledSelect defaultValue="" onChange={ value => props.onChangeProject(value as string) }>
            <Option value="">All</Option>
            { props.projects.map(project => {
                return <Option key={ project } value={ project }>{ project }</Option>
            })}
        </StyledSelect>
    </StyledSelectForm>
}

export { SpidersFilterProjectProps }
export default SpidersFilterProject