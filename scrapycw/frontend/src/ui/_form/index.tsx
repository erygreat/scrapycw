// import React from "react";
// import style from "./index.module.css";

// interface ItemProps {
//     label: string,
//     children: JSX.Element,
//     hasColon: boolean,
//     labelClass?: string,
//     itemClass?: string,
//     contentClass?: string,
// }
// const Item = (props: ItemProps) => {
//     return <div className={`${style.item} ${props.itemClass}`}>
//         <div className={`${style.label} ${props.labelClass}`}>{ props.label }{ props.hasColon ? ':' : '' }</div>
//         <div className={`${style.value} ${props.contentClass}`}>{ props.children }</div>
//     </div>
// }
// Item.defaultProps = {
//     hasColon: true,
//     labelClass: '',
//     itemClass: '',
//     contentClass: '',
// }
// export const Form = {
//     Item
// }