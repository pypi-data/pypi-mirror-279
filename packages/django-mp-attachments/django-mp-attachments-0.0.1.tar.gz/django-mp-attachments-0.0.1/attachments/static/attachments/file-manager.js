
FileManager = class {
    constructor({
        $input,
        removeMessage,
        uploadUrl,
    }) {
        const $container = $('[data-role=images-container]');
        const $dropLinkSection = $container.find('[data-role=drop-link-section]');
        const $dropFilesSection = $container.find('[data-role=drop-files-section]');
        const $files = $container.find('[data-role=files]');

        this._$input = $input;
        this._$files = $files;
        this._uploadUrl = uploadUrl;
        this._removeMessage = removeMessage;
        
        new Dropzone($dropFilesSection[0], {
            url: uploadUrl,
            createImageThumbnails: false,
            acceptedFiles: 'image/*',
            parallelUploads: 5,
            resizeWidth: 2000,
            resizeHeight: 2000,
            resizeQuality: 0.8,
            addedfile: (file) => this._renderPreloader(file.upload.uuid),
            success: (file, response) => {
                $files.find('[data-uuid=' + file.upload.uuid + ']').remove();
                const items = this._getItems();
                const maxOrder = items.length ? Math.max(...items.map(i => i.order)) : -1;
                const item = {...response, order: maxOrder + 1};
                items.push(item);
                this._setItems(items);
                this._renderFile(item);
            },
            error: (file, response) => console.log(response)
        });
    
        $files.sortable({
            items:'.file-preview',
            cursor: 'move',
            opacity: 0.7,
            distance: 20,
            tolerance: 'pointer',
            update: (event, ui) => {
                $input.empty();
                const newItems = [];
                $files.find('.file-preview').each((i, preview) => {
                    const item = $(preview).data('item');
                    item.order = i;
                    newItems.push(item);
                });
                this._setItems(newItems);
            }
        });
        
        this._renderFiles();

        const $html = $('html');
        $html.on('dragover', this._stopEvent);
        $html.on('dragleave', this._stopEvent);
        
        $dropLinkSection.on('drop', this._handleLinkSectionDrop);
    }
    
    _renderFiles = () => {
        this._$input.empty();
        this._getItems().forEach(this._renderFile)
    }
    
    _renderFile = (item) => {
        const $file = $('<div />').addClass('file-preview').data("item", item);
        const $img = $('<img />').prop('src', item.preview_url);
        const $removeBtn = $('<button type="button" />').addClass('remove-btn');

        $file.append($img);
        $file.append($removeBtn);

        this._$files.append($file);

        $removeBtn.click((e) => {
            if (confirm(this._removeMessage)) {
                this._setItems(this._getItems().filter(i => i.uuid !== item.uuid))
                $file.remove();
            }
        });
    }
    
    _renderPreloader = (uuid) => {
        this._$files.append(
            `<div data-uuid="${uuid}" class="preloader">` +
            `    <img src="/static/file-manager/spinner.gif" />` +
            `</div>`
        );
    }
    
    _handleLinkSectionDrop = (event) => {
        const html = event.originalEvent.dataTransfer.getData('text/html');
        const url = $('<div />').html(html).find("img").attr('src');
        const data = {url};
        
        $.post(
            this._uploadUrl,
            data
        ).success((response) => {
            this._renderFile(response);
        }).fail((response) => console.log(response));
    }
    
    _stopEvent = (event) => {
        event.preventDefault();
        event.stopPropagation();
    }

    _getItems = () => {
        return JSON.parse(this._$input.val());
    }

    _setItems = (items) => {
        this._$input.val(JSON.stringify(items));
    }
}
