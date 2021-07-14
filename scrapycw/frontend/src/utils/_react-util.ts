import React from "react";

const ReactUtil = {
    isDomTypeElement: (element: React.ReactElement) => {
        return React.isValidElement(element) && typeof element.type === "string";
    },
    isReactComponent: (element: React.ReactNode) => {
        return React.isValidElement(element) && typeof element.type === 'function';
    },
    isFunctionComponent: (element: React.ReactElement) => {
        return typeof element.type === 'function' && String(element).includes('return React.createElement');
    },
    isClassComponent: (element: React.ReactElement) => {
        return typeof element.type === 'function' && !!element.type.prototype.isReactComponent;
    },
}
export default ReactUtil;