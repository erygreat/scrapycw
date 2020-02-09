import React, {FC, useState, useCallback} from 'react';
import { LeftCircleOutlined, RightCircleOutlined, SoundFilled } from '@ant-design/icons';

interface CollapseBtnProps {
  openCollapse: Function;
  closeCollapse: Function;
}

const CollapseBtn: FC<CollapseBtnProps & React.HTMLAttributes<HTMLDivElement>> = props => {
  const [collapse, setCollapse] = useState(true);
  const changeCollapse = useCallback(status => {
      setCollapse(status)
      if(status) {
          if(typeof props.openCollapse === "function") {
            props.openCollapse(status);
          }
      } else {
          if(typeof props.closeCollapse === "function") {
            props.closeCollapse(status);
          }
      }
  }, []);
  
  return (
    <div className={ props.className }>
    {collapse 
        ? <LeftCircleOutlined onClick={() => { changeCollapse(false)}}/> 
        : <RightCircleOutlined onClick={() => { changeCollapse(true)}}/>
    }
    </div>
  )
}

export default CollapseBtn;
