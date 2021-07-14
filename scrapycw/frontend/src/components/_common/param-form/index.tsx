// import { Input, Tooltip } from '@/components/ui';
// import { QuestionCircleOutlined } from '@ant-design/icons';
// import React, { FC, useState } from 'react';
// import style from "./index.module.css"
// import { format as argvFormat } from "@/utils/argv";
// import { ParamFormProps } from './types';

// const ParamForm: FC<ParamFormProps> = (props: ParamFormProps): JSX.Element => {
//     const [settings, setSettings] = useState<string>('');
//     const [showError, setShowError] = useState<boolean>(false);

//     const handleBlur = () => {
//         let hasError = false;
//         if (props.verify) {
//             hasError = !props.verify(settings);
//             setShowError(Boolean(props.isShowError) && hasError);
//         }
//         let result = argvFormat(settings);
//         props.onBlur(result, hasError);
//     }

//     return <>
//         <Input.TextArea placeholder={props.placeholder} value={settings} onChange={e => setSettings(e.target.value)} onBlur={() => { handleBlur() }} autoSize={{ minRows: 3 }} />
//         <Tooltip title="暂不支持“字典”和“列表”，后续会添加对该类型的支持！">
//             <span className={style.tip}>
//                 <QuestionCircleOutlined />
//             </span>
//         </Tooltip>
//         {showError ? <div className={style.error}>格式错误, 请检查!</div> : <></>}
//     </>
// }
// export { ParamForm }