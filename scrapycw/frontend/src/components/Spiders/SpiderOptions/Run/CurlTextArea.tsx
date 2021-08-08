import { Input } from "@ui";
import { FC } from "react";

interface CurlFormProps {
    command: string;
}

const CurlForm: FC<CurlFormProps> = props => {
    return <Input.TextArea value={props.command} autoSize={{ minRows: 3 }} disabled/>
}

export default CurlForm;