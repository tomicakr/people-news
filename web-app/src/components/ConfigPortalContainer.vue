<template>
  <div>
    <div class="upper">
      <button class="add-new" @click="saveChanges">Spremi promjene</button>
      <textarea v-if="successCode !== ''" class="successArea" v-model="successCode" readonly></textarea>
    </div>
    <prism-editor class="my-editor" v-model="code" :highlight="highlighter" line-numbers></prism-editor>
    <textarea v-if="errorCode !== ''" class="errorArea" v-model="errorCode" readonly></textarea>
  </div>
</template>
 
<script>
  import { PrismEditor } from 'vue-prism-editor'
  import 'vue-prism-editor/dist/prismeditor.min.css'
  import { highlight, languages } from 'prismjs/components/prism-core'
  import 'prismjs/components/prism-clike'
  import 'prismjs/components/prism-javascript'
  import 'prismjs/themes/prism-tomorrow.css'
  import axios from 'axios'
 
  export default {
    components: {
      PrismEditor,
    },
    /* eslint-disable*/
    data: function () {
      return { 
        code: `function fn() {
    return {
      vecernji: {
        url: 'http://vecernji.hr/vijesti/',
        evalString: '//a[starts-with(@href, "/vijesti/")]',
        titleString: '.article__title',
        contentString: '.article__body--main_content',
        filters: [
            containsRegex(/-\d+$/),
            removeDuplicates
        ],
        async specificTextGetter(page) {
            const paragraphs = await page.$x('//div[@class="article__body--main_content"]//p');
            let content = [];
            for (let i = 0; i < paragraphs.length; i++) {
                const p = await paragraphs[i].getProperty('textContent');
                const text = p._remoteObject.value && p._remoteObject.value.trim();
                if (text) content.push(text);
            }
            
            return content;
        }
      }
    }
  }`,
         errorCode: '',
         successCode: ''
      }
    },
    /* eslint-enable*/
    methods: {
      highlighter(code) {
        return highlight(code, languages.js)
      },
      async saveChanges() {
        try {
          eval(this.code);
          this.errorCode = ''
          this.successCode = 'To je valjani JavaScript kod. Promjene su spremljene...'
        } catch (e) {
          this.successCode = ''
          this.errorCode = 'To nije valjani JavaScript kod. Provjerite još jednom:\n' + e
        }
        await axios.post(`http://localhost:3000/new_portal`, { code: this.code })
      }
    },
  };
</script> 
 
<style>
/* required class */
.my-editor {
  /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
  background: #2d2d2d;
  color: #ccc;

  /* you must provide font-family font-size line-height. Example: */
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px;
}

/* optional class for removing the outline */
.prism-editor__textarea:focus {
  outline: none;
}

.errorArea {
  width: 100%;
  height: 50px;
  background-color: red;
}

.successArea {
  width: 80%;
  height: 30px;
  background-color: green;
  margin-left: 10px;
}

.add-new {
  margin-bottom: 2px;
  cursor: pointer;
  font-weight: 600;
}

.add-new:hover {
  transform: scale(1.12);
}

.upper {
  display: flex;
}
</style> 