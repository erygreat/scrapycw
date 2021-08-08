import BaseTextArea, { BaseTextAreaEvent } from "./BaseTextArea";
import { FC } from "react";

const placeholder = `-a color=blue
-a page=10
`

const ArgumentTextArea: FC<BaseTextAreaEvent> = props => {
    return <BaseTextArea pattern="-a" placeholder={ placeholder } { ...props } />
}
export default ArgumentTextArea;