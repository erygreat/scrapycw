// import React, {FC, useState} from 'react';
// import { ParamForm } from "@/components/common/param-form";
// import { verify as argvVerify} from "@/utils/argv";
// import { SettingsFormProps } from './types';

// const settingsPlaceholder = `-s ROBOTSTXT_OBEY=True
// -s REDIRECT_MAX_TIMES=10
// -s LOG_LEVEL='INFO'
// -s LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'
// `

// const SettingsForm: FC<SettingsFormProps> = (props) => {
//     const verify = (text: string) => {
//         try {
//             argvVerify(text, '-s');
//         } catch(e) {
//             return false;
//         }
//         return true;
//     }

//     return <ParamForm 
//     onBlur={(text, hasError) => { props.onInputEnd(text, hasError) }} isShowError placeholder={ settingsPlaceholder } verify={verify}></ParamForm>
// }
// export { SettingsForm }