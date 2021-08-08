import styled from "styled-components";

interface ItemProps {
    label: string,
    children: JSX.Element,
    hasColon: boolean,
    labelClass?: string,
    itemClass?: string,
    contentClass?: string,
}

const StyledItemLabel = styled.div`
    line-height: 32px;
    font-weight: 600;
    align-self: start;
`

const StyledItemContent = styled.div`

`

const StyledItem = styled.div`
    display: flex;
    padding: 10px 0;
    min-height: 32px;
    align-items: center;
`

const FormItem = (props: React.HTMLAttributes<HTMLDivElement> & ItemProps) => {
    return <StyledItem className={ `${ props.itemClass } ${ props.className }` }>
        <StyledItemLabel className={ props.labelClass }>{ props.label }{ props.hasColon ? ':' : '' }</StyledItemLabel>
        <StyledItemContent className={ props.contentClass }>{ props.children }</StyledItemContent>
    </StyledItem>
}

FormItem.defaultProps = {
    hasColon: true,
    labelClass: '',
    itemClass: '',
    contentClass: '',
}

FormItem.StyledItem = StyledItem;
FormItem.StyledItemLabel = StyledItemLabel;
FormItem.StyledItemContent = StyledItemContent;

export default FormItem