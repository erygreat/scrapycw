import React, {FC} from 'react';
import { ParamForm } from "@/components/common/param-form";
import { verify as argvVerify} from "@/utils/argv";
import { ArgumentFormProps } from './types';

const argumentPlaceholder = `-a color=blue
-a page=10
`
const ArgumentForm: FC<ArgumentFormProps> = (props) => {
    const verify = (text: string) => {
        try {
            argvVerify(text, '-a');
        } catch(e) {
            return false;
        }
        return true;
    }

    return <ParamForm 
    onBlur={(text, hasError) => { props.onInputEnd(text, hasError) }} isShowError placeholder={ argumentPlaceholder } verify={verify}></ParamForm>
}
export { ArgumentForm }