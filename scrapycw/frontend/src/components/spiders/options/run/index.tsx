import { DataSpider } from '@/components/spiders/types';
import { Button, Modal, Form, Input, message, confirm, Loading } from '@/components/ui';
import style from './index.module.css';
import React, {FC, useState} from 'react';
import { SettingsForm } from '@/components/common/settings-form';
import { ArgumentForm } from '@/components/common/argument-form';
import copy from 'copy-to-clipboard';
import { group } from '@/utils/argv';
import { runSpider } from '@/utils/scrapycw';
import { CurlFormProps, RunnerModalProps } from "./types";


const CurlForm: FC<CurlFormProps> = props => {
    return <Input.TextArea value={props.command} autoSize={{ minRows: 3 }} disabled/>
}

let settingText: string | null = null;
let settingHasError = false;
let settingObj: {
    [propName: string]: any;
} | null = null
let argumentText: string | null = null;
let argumentHasError = false;
let argumentObj: {
    [propName: string]: any;
} | null = null
const RunnerModal: FC<DataSpider & RunnerModalProps> = props => {

    const generateCommand = () => {
        let text: string = 'scrapycw crawl ' + props.spider + " -p " + props.project;
        if(!settingHasError && settingText) {
            text = text + ' ' + settingText;
        }
        if(!argumentHasError && argumentText) {
            text = text + ' ' + argumentText;
        }
        if(text) {
            text = text;
        }
        return text;
    }

    const [command, setCommand] = useState(generateCommand());
    const [hasError, setHasError] = useState(false);
    const [closeClear, setCloseClear] = useState(false);
    const [loading, setLoading] = useState(false);

    const copyText = () => {
        copy(command);
        message.success("复制成功!");
    }
    const settingsEnter = (text: string, hasError: boolean) => {
        settingText = text;
        settingHasError = hasError;
        let newCommand = generateCommand();
        setCommand(newCommand);
        setHasError(settingHasError || argumentHasError);
        settingObj = group(text, '-s');
    }
    const argumentEnter = (text: string, hasError: boolean) => {
        argumentText = text;
        argumentHasError = hasError;
        let newCommand = generateCommand();
        setCommand(newCommand);
        setHasError(settingHasError || argumentHasError);
        argumentObj = group(text, '-a');
    }
    const handleCancel = () => {
        setCloseClear(false);
        props.hide();
    }
    const handleOk = () => {
        confirm({
            text: "确认要执行爬虫？",
            onOk() {
                setLoading(true);
                runSpider({
                    spider: props.spider,
                    project: props.project,
                    settings: settingObj,
                    spargs: argumentObj,
                    onSuccess() {
                        setCloseClear(true);
                        setLoading(false);
                        props.hide();
                        message.success("运行成功！");
                    },
                    onError(msg, httpCode, serverCode) {
                        message.error(msg);
                        setLoading(false);
                    },
                })
            },
        })
    }
    return <>
        <Modal width={750} visible={props.isVisible} destroyOnClose={closeClear} onOk={handleOk} onCancel={handleCancel} cancelText="取消" okText="运行" closable={false} footer={null} maskClosable={false}>
            <Loading tip="请求中..." spinning={loading} delay={100}>
                <Form.Item label="所属项目" labelClass={style.label}>
                    <Input disabled value={props.project}></Input>
                </Form.Item>
                <Form.Item label="爬虫名称" labelClass={style.label}>
                    <Input disabled value={props.spider}></Input>
                </Form.Item>
                <Form.Item label="Settings" labelClass={style.label} contentClass={style.settingsContent}>
                    <SettingsForm onInputEnd={ (text, hasError) => { settingsEnter(text, hasError) }}></SettingsForm>
                </Form.Item>
                <Form.Item label="Argument" labelClass={style.label} contentClass={style.settingsContent}>
                    <ArgumentForm onInputEnd={ (text, hasError) => { argumentEnter(text, hasError) }}></ArgumentForm>
                </Form.Item>
                <Form.Item label="命令行" labelClass={style.label} contentClass={style.settingsContent}>
                    <CurlForm command={ command }></CurlForm>
                </Form.Item>
                <div className={style.btnGroup}>
                    <Button className={style.controlBtn} type="primary" onClick={ handleOk } disabled={hasError}>运行</Button>
                    <Button className={style.controlBtn} type="primary" onClick={ copyText } disabled={hasError}>复制命令到剪切板</Button>
                    <Button className={style.controlBtn} onClick={ handleCancel }>取消</Button>
                </div>
            </Loading>
        </Modal>
    </>
}
export default RunnerModal;
