from linebot.v3.messaging import (
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)

def GenerateQuickBottom():
    quickReply = QuickReply(
        items=[
            QuickReplyItem(
                action=PostbackAction(
                    label="Account book",
                    data="postback",
                    #display_text="postback"
                ),
                #image_url=postback_icon
            ),
            QuickReplyItem(
                action=MessageAction(
                    label="Message",
                    text="message"
                ),
                #image_url=message_icon
            ),
            QuickReplyItem(
                action=DatetimePickerAction(
                    label="Date",
                    data="date",
                    mode="date"
                ),
                #image_url=date_icon
            ),
            QuickReplyItem(
                action=DatetimePickerAction(
                    label="Time",
                    data="time",
                    mode="time"
                ),
                #image_url=time_icon
            ),
            QuickReplyItem(
                action=DatetimePickerAction(
                    label="Datetime",
                    data="datetime",
                    mode="datetime",
                    initial="2024-01-01T00:00",
                    max="2025-01-01T00:00",
                    min="2023-01-01T00:00"
                ),
                #image_url=datetime_icon
            ),
            QuickReplyItem(
                action=CameraAction(label="Camera")
            ),
            QuickReplyItem(
                action=CameraRollAction(label="Camera Roll")
            ),
            QuickReplyItem(
                action=LocationAction(label="Location")
            )
        ]
    )
    return quickReply

def GenerateYesNoQuickBottom():
    quickReply = QuickReply(
        items=[
            QuickReplyItem(
                action=PostbackAction(
                    label="Yes",
                    data="Continue accounting mode",
                    display_text="記帳"
                ),
                #image_url=postback_icon
            ),
            QuickReplyItem(
                action=PostbackAction(
                    label="No",
                    data="Quit accounting mode",
                    #display_text="postback"
                ),
                #image_url=postback_icon
            )
        ]
    )
    return quickReply
def GenerateModeQuickBottom():
    quickReply = QuickReply(
        items=[
             QuickReplyItem(
                action=PostbackAction(
                    label="Audit(查帳)",
                    data="Audit",
                    display_text="查帳"
                ),
                #image_url=postback_icon
            ), QuickReplyItem(
                action=PostbackAction(
                    label="Delete data(刪除)",
                    data="Delete",
                    display_text="刪除"
                ),
                #image_url=postback_icon
            ), QuickReplyItem(
                action=PostbackAction(
                    label="Quit accounting(離開)",
                    data="Quit accounting mode",
                    #display_text="postback"
                ),
                #image_url=postback_icon
            ) 
        ]        
    )
    return quickReply

def GenerateAuditYesNoQuickBottom():
    quickReply = QuickReply(
        items=[
            QuickReplyItem(
                action=PostbackAction(
                    label="Yes",
                    data="Continue audit mode",
                    display_text="查帳"
                ),
                #image_url=postback_icon
            ), QuickReplyItem(
                action=PostbackAction(
                    label="No",
                    data="Quit audit mode",
                    #display_text="postback"
                ),
                #image_url=postback_icon
            ),QuickReplyItem(
                action=PostbackAction(
                    label="Delete(刪除)",
                    data="Continue delete mode",
                    display_text="刪除"
                ),
                #image_url=postback_icon
            )
        ]
    )
    return quickReply

def GenerateDeleteYesNoQuickBottom():
    quickReply = QuickReply(
        items=[
            QuickReplyItem(
                action=PostbackAction(
                    label="Yes",
                    data="Continue delete mode",
                    display_text="刪除"
                ),
                #image_url=postback_icon
            ),
            QuickReplyItem(
                action=PostbackAction(
                    label="No",
                    data="Quit delete mode",
                    #display_text="postback"
                ),
                #image_url=postback_icon
            )
        ]
    )
    return quickReply
