window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor
    const divs = document.querySelectorAll('.wang-editor-tools')
    for (let i = 0; i < divs.length; i++) {
        const container_id = divs[i].getAttribute('data-container-id')
        const custom_editor_config = JSON.parse(divs[i].getAttribute('data-editor-config'))
        const custom_toolbar_config = JSON.parse(divs[i].getAttribute('data-toolbar-config'))
        const textarea = document.querySelector(`#${container_id}`)
        const editorConfig = {
            placeholder: '请输入内容',
            MENU_CONF: {
                // 图片上传配置
                uploadImage: {
                    server: '/wang_editor/upload/image/',
                },
                // 上传视频配置
                uploadVideo: {
                    server: '/wang_editor/upload/video/',
                },
            },
            onChange(editor) {
                // const html = editor.getHtml()
                textarea.value = editor.getHtml()
            },
            ...custom_editor_config
        }

        const editor = createEditor({
            selector: `#editor-container-${container_id}`,
            html: textarea.value,
            config: editorConfig,
            mode: 'default', // or 'simple'
        })

        const toolbarConfig = {
            // 自定义配置
            ...custom_toolbar_config
        }

        const toolbar = createToolbar({
            editor,
            selector: `#toolbar-container-${container_id}`,
            config: toolbarConfig,
            mode: 'default', // or 'simple'
        })
    }
}