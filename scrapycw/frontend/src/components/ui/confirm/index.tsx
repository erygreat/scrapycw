import Notification from 'rc-notification';
import { NotificationInstance } from 'rc-notification/lib/Notification';
import React from 'react';
import style from "./index.module.css";
import { Button } from "@/components/ui";

interface ConfirmOptions {
  title?: string,
  text?: string | JSX.Element,
  onOk?: () => void,
  onCancel?: () => void,
}
export const confirm = (options: ConfirmOptions) => {
  let currentNotification: NotificationInstance | null = null;
  const close = () => {
    if(currentNotification) {
      currentNotification.destroy();
    }
    return true;
  }

  const handleOk = () => {
    close();
    if(options.onOk) {
      options.onOk()
    }
  }

  const handleCancel = () => {
    close();
    if(options.onCancel) {
      options.onCancel()
    }
  }

  Notification.newInstance({
    maxCount: 1,
    prefixCls: style.noticeContainer,
    style: {
      top: 0,
      left: 0
    }
  }, notification => {
    currentNotification = notification;
    notification.notice({
      content: <div className={style.notice}>
        <h3 className={style.title}>{options.title || '提示'}</h3>
        <div className={style.content}>{options.text}</div>
        <div className={style.btnGroup}>
          <Button className={style.btn} type="primary" size="small" onClick={ handleOk }>确认</Button>
          <Button className={style.btn} size="small" onClick={ handleCancel }>取消</Button>
        </div>
      </div>,
    });
  });
};