<template>
    <div>
        <iframe class="iframe" :src="pdf_url"></iframe>
    </div>
</template>

<script>
export default {
    data() {
        return {
            pdf_url: "user_manual.pdf"
        }
    }
}
</script>

<style>
.iframe{
    margin-top: 5px;
    height: 95vh;
    width: 100vw;
}
</style>