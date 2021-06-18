let clearCanvas = function () {
    pol = []
    ctx.closePath();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
}

let app = new Vue({
    el: '#App',
    mounted() {
        var c = document.getElementById("polygon");
        this.vueCanvas = c.getContext("2d");
        this.vueCanvas.beginPath();
        this.vueCanvas.strokeStyle = '#32a852';
        this.vueCanvas.canvas.width = 500;
        this.vueCanvas.canvas.height = 500;
        this.is_last_point = false;
    },
    data: {
        pol: [],
        currX: null,
        currY: null,
        prevX: null,
        prevY: null,
        last_point: null,
        is_last_point: null,
        testMsg: 'Hello',
        state_msg: null,
        for_save: false
    },
    computed: {},
    watch: {
        is_last_point(state) {
            this.state_msg = state
                ? "Укажите проверяемую точку"
                : "Строим полигон"
        }
    },
    methods: {
        canvasPoint(event) {
            if (this.pol.length > 10 && !this.is_last_point) {
                this.state_msg = "Много точек!"
                return null
            }
            let x = event.offsetX;
            let y = event.offsetY - 50;
            this.vueCanvas.moveTo(x, y);
            this.is_last_point
                ? this.last_point = [x, y]
                : this.pol.push([x, y])
            console.log(this.pol)
            this.vueCanvas.arc(x, y, 1, 0, 360, false);
            this.vueCanvas.stroke();
        },
        move(event) {
            this.prevX = this.currX;
            this.prevY = this.currY;

            this.currX = event.offsetX;
            this.currY = event.offsetY;
        },
        canvasComplete() {
            this.pol.forEach(item => this.vueCanvas.lineTo(item[0], item[1]))
            this.is_last_point = true;
            this.vueCanvas.stroke();
            this.vueCanvas.closePath();
        },
        canvasClear() {
            window.location.reload(true);
        }
    },
})