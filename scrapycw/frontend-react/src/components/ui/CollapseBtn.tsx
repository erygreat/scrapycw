import React, {FC, useState, useCallback} from 'react';
import { LeftCircleOutlined, RightCircleOutlined } from '@ant-design/icons';
import * as helpStyles from "@/stylesheets/help.module.css";

interface CollapseBtnProps {
  openCollapse: Function;
  closeCollapse: Function   ;
}
const CollapseBtn: FC<CollapseBtnProps> = props => {
  const [collapse, setCollapse] = useState(true);
  const changeCollapse = useCallback(status => {
      setCollapse(status)
      if(status) {
          if(typeof props.openCollapse === "function") {
            props.openCollapse();
          }
      } else {
          if(typeof props.closeCollapse === "function") {
            props.closeCollapse();
          }
      }
  }, []);
  
  return (
    <>
    {collapse 
        ? <LeftCircleOutlined onClick={() => { changeCollapse(false)}}/> 
        : <RightCircleOutlined onClick={() => { changeCollapse(true)}}/>
    }
    </>
  )
}

export default CollapseBtn;
