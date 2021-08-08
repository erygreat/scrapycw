import ArgvTextArea from "@/components/common/ArgvTextArea";
import { verify as argvVerify} from "@/utils/argv";
import { FC } from "react";

interface BaseTextAreaEvent {
    onInputEnd(text: string, hasError: boolean): void,
}

type BaseTextAreaProps = BaseTextAreaEvent & {
    pattern: string
    placeholder?: string
}

const BaseTextArea: FC<BaseTextAreaProps> = props => {
    const verify = (text: string) => {
        try {
            argvVerify(text, props.pattern);
        } catch(e) {
            return false;
        }
        return true;
    }

    return <ArgvTextArea
        onBlur={(text, hasError) => { props.onInputEnd(text, hasError) }}
        isShowError
        placeholder={ props.placeholder }
        verify={ verify }
    />
}

export { BaseTextAreaEvent }
export default BaseTextArea;