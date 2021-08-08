import { FC, useState } from 'react';
import { format as argvFormat } from "@/utils/argv";
import { Input } from "@ui"
import styled from 'styled-components';

export interface ArgvTextAreaProps {
    placeholder?: string,
    onBlur: (text: string, hasError: boolean) => void,
    verify?: (text: string) => boolean,
    isShowError?: boolean
}

const StyledError = styled.div`
    padding: 5px 0;
    color: red;
`

const ArgvTextArea: FC<ArgvTextAreaProps> = props => {
    const [value, setValue] = useState<string>('');
    const [showError, setShowError] = useState<boolean>(false);

    const handleBlur = () => {
        let hasError = false;
        if (props.verify) {
            hasError = !props.verify(value);
            setShowError(Boolean(props.isShowError) && hasError);
        }
        const result = argvFormat(value);
        props.onBlur(result, hasError);
    }

    return <>
        <Input.TextArea placeholder={ props.placeholder } value={ value } onChange={e => setValue(e.target.value)} onBlur={() => { handleBlur() }} autoSize={{ minRows: 3 }} />
        {showError ? <StyledError>格式错误, 请检查!</StyledError> : <></>}
    </>
}
export default ArgvTextArea