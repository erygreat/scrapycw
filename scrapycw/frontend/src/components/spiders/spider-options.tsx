import React, {FC, useState} from 'react';
import { DataSpider } from './types';
import { Button, Modal, Form, Input, Switch } from '@/components/ui';

interface SpiderRunnerModalProps {
    isVisible: boolean,
    hide(): void,
}
const SpiderRunnerModal: FC<DataSpider & SpiderRunnerModalProps> = props => {
    const [settings, setSettings] = useState('');
    const handleCancel = () => {
        props.hide();
    }
    const handleOk = () => {
        // TODO 运行爬虫
        props.hide();
    }
    return <>
        <Modal visible={props.isVisible} onOk={handleOk} onCancel={handleCancel} cancelText="取消" okText="运行" closable={false} maskClosable={false}>
            <Form.Item label="所属项目">
                <Input disabled value={props.project}></Input>
            </Form.Item>
            <Form.Item label="爬虫名称">
                <Input disabled value={props.spider}></Input>
            </Form.Item>
            <Form.Item label="Settings">
                <Switch />
            </Form.Item>
            <Form.Item label="">
                <div>
                    <div>
                    
                    </div>
                <Input.TextArea value={settings} onChange={e => setSettings(e.target.value)}/>
                </div>
            </Form.Item>
        </Modal>
    </>
}

export const SpiderOptions: FC<DataSpider> = props => {
    const [visibleRunModel, setVisibleRunModel] = useState(false);
    return <div>
        <Button type="primary" size="small" onClick={() => setVisibleRunModel(true) }>运行</Button>
        <SpiderRunnerModal isVisible={visibleRunModel} hide={() => setVisibleRunModel(false)} {...props}></SpiderRunnerModal>
    </div>
}