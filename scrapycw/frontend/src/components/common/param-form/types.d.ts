export interface ParamFormProps {
    placeholder?: string,
    onBlur: (text: string, hasError: boolean) => void,
    verify?: (text: string) => boolean,
    isShowError?: boolean
}