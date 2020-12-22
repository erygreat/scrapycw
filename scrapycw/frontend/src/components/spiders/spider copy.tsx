// import React, {FC, useEffect, useState} from 'react';
// import { Table } from '@/components/ui';
// import { Button, Modal, Form, Input } from '@/components/ui';
// import axios from 'axios';
// import { Response } from "@/components/types";

// interface SpiderInfo {
//     project: string,
//     spider: string,
// }
// interface SpiderRunnerModalProps {
//     isVisible: boolean,
//     hide(): void,
// }
// const SpiderRunnerModal: FC<SpiderInfo & SpiderRunnerModalProps> = props => {
//     const [settings, setSettings] = useState('');
//     const handleCancel = () => {
//         props.hide();
//     }
//     const handleOk = () => {
//         // TODO 运行结果
//         props.hide();
//     }
//     return <>
//         <Modal visible={props.isVisible} onOk={handleOk} onCancel={handleCancel} cancelText="取消" okText="运行" closable={false}>
//             <Form>
//                 <Form.Item label="所属项目">
//                     <Input disabled value={props.project}></Input>
//                 </Form.Item>
//                 <Form.Item label="爬虫名称">
//                     <Input disabled value={props.spider}></Input>
//                 </Form.Item>
//                 <Form.Item label="Settings">
//                     <div>
                        
//                     </div>
//                     1111
//                     <Input.TextArea value={settings} onChange={e => setSettings(e.target.value)}/>
//                 </Form.Item>
//             </Form>
//         </Modal>
//     </>
// }
