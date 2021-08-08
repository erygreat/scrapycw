import ArgvTextArea from "@/components/common/ArgvTextArea";
import { FC } from "react";
import BaseTextArea, { BaseTextAreaEvent } from "./BaseTextArea";

const placeholder = `-s ROBOTSTXT_OBEY=True
-s REDIRECT_MAX_TIMES=10
-s LOG_LEVEL='INFO'
-s LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'
`

const ArgumentTextArea: FC<BaseTextAreaEvent> = props => {
    return <BaseTextArea pattern="-s" placeholder={ placeholder } { ...props } />
}

export default ArgumentTextArea;