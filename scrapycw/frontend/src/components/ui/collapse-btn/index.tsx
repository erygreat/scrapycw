import React, {FC, useState, useCallback} from 'react';
import { LeftCircleOutlined, RightCircleOutlined } from '@ant-design/icons';
interface CollapseBtnProps {
  openCollapse(): void;
  closeCollapse(): void;
}

export const CollapseBtn: FC<CollapseBtnProps & React.HTMLAttributes<HTMLDivElement>> = props => {
  const [collapse, setCollapse] = useState(true);
  const changeCollapse = useCallback(status => {
      setCollapse(status)
      if(status) {
          props.openCollapse();
      } else {
          props.closeCollapse();
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