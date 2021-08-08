import { FC, useRef, useState } from "react";
import { Modal, Input, Button, message, confirm, Loading, FormItem } from "@ui";
import { SpiderData } from "../../types.d";
import styled from "styled-components";
import SettingsTextArea from "./SettingsTextArea";
import ArgumentTextArea from "./ArgumentTextArea";
import CurlTextArea from "./CurlTextArea"
import copy from 'copy-to-clipboard';
import { group as argvGroup } from '@/utils/argv';
import interfaces from "@/interfaces";

interface RunnerModalProps {
    spider: SpiderData
    isVisible: boolean
    hide: () => void
}

const StyledInputShort = styled(Input)`
    width: 200px;
`

type ModalFormProps = SpiderData & {
    handlerCancel: () => void
    handlerOk: () => void
}

const StyledButtonGroup = styled.div`
    text-align: center;
`

const StyledButton = styled(Button)`
    margin: 0 10px;
`

const ModalItem = styled(FormItem)`
    ${ FormItem.StyledItemLabel } {
        width: 80px;
    }
    ${ FormItem.StyledItemContent } {
        width: 500px;
    }
`

const ModalForm: FC<ModalFormProps> = props => {

    const settingsRef = useRef<string>('');
    const settingsHasErrorRef = useRef<boolean>(false);
    const argumentRef = useRef<string>('');
    const argumentHasErrorRef = useRef<boolean>(false);
    const [hasError, setHasError] = useState(false);
    const [loading, setLoading] = useState(false);

    const generateCommand = () => {
        let text = 'scrapycw crawl ' + props.spider + " -p " + props.project;
        if(!settingsHasErrorRef.current && settingsRef.current) {
            text = text + ' ' + settingsRef.current;
        }
        if(!argumentHasErrorRef.current && argumentRef.current) {
            text = text + ' ' + argumentRef.current;
        }
        if(text) {
            text = text;
        }
        return text;
    }

    const [command, setCommand] = useState(generateCommand());

    const copyText = () => {
        copy(command);
        message.success("复制成功!");
    }

    const handleOk = () => {
        confirm({
            text: "确认要执行爬虫？",
            onOk: async () => {
                setLoading(true);
                const settings = argvGroup(settingsRef.current, '-s');
                const argument = argvGroup(argumentRef.current, '-a');
                const response = await interfaces.runSpider({
                    spider: props.spider,
                    project: props.project,
                    settings: settings,
                    spargs: argument
                })

                if(response.success) {
                    props.handlerOk();
                    setLoading(false);
                    message.success("运行成功！");
                } else {
                    message.error(response.message);
                    setLoading(false);
                }
            },
        })
    }

    const handlerSettings = (text: string, hasError: boolean) => {
        settingsRef.current = text;
        settingsHasErrorRef.current = hasError;
        setCommand(generateCommand());
        setHasError(settingsHasErrorRef.current || argumentHasErrorRef.current);
    }

    const handlerArgument = (text: string, hasError: boolean) => {
        argumentRef.current = text;
        argumentHasErrorRef.current = hasError;
        setCommand(generateCommand());
        setHasError(settingsHasErrorRef.current || argumentHasErrorRef.current);
    }

    return <Loading tip="请求中..." spinning={loading} delay={100}>
        <ModalItem label="所属项目">
            <StyledInputShort disabled value={ props.project } />
        </ModalItem>
        <ModalItem label="爬虫名称">
            <StyledInputShort disabled value={props.spider} />
        </ModalItem>
        <ModalItem label="Settings">
            <SettingsTextArea onInputEnd={ (text, hasError) => { handlerSettings(text, hasError) }} />
        </ModalItem>
        <ModalItem label="Argument">
            <ArgumentTextArea onInputEnd={ (text, hasError) => { handlerArgument(text, hasError) }} />   
        </ModalItem>
        <ModalItem label="命令行">
            <CurlTextArea command={ command } />
        </ModalItem>

        <StyledButtonGroup>
            <StyledButton type="primary" onClick={ handleOk } disabled={ hasError }>运行</StyledButton>
            <StyledButton type="primary" onClick={ copyText } disabled={ hasError }>复制命令到剪切板</StyledButton>
            <StyledButton onClick={ props.handlerCancel }>取消</StyledButton>
        </StyledButtonGroup>
    </Loading>
}

const RunnerModal: FC<RunnerModalProps> = props => {

    const [closeClear, setCloseClear] = useState(false);

    const handlerCancel = () => {
        setCloseClear(false);
        props.hide();
    }

    const handlerOk = () => {
        setCloseClear(true);
        props.hide();
    }

    return <Modal width={ 750 } visible={ props.isVisible } destroyOnClose={ closeClear } onCancel={ handlerCancel } cancelText="取消" okText="运行" closable={ false } footer={ null } maskClosable={ false }>
        <ModalForm { ...props.spider } handlerCancel={ handlerCancel } handlerOk={ handlerOk }/>
    </Modal>
}

export { RunnerModalProps }
export default RunnerModal;
