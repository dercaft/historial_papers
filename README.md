# 历史论文收集翻译

给女票的史料汇编做的自动化小项目

## Requirement:

- Python
- beautifulsoup4
- requests
- python-docx

详细的依赖包列表可见：[./requirement.yaml](./requirement.yaml)

如何使用：

1. 使用 SingleFile插件，保存网页成离线的html文件，并记录到.csv表格中（格式仿照papers.csv）

2.  将DeepL账号密码写进 translate.py 文件里

3. 运行python文件 main.py

```shell
python main.py <name>.csv
```

## 总体思路：

从树状结构的网页html中将文本抽取出来，

本项目的主要程序是一种状态机，在遍历html DOM树的过程中，根据当前节点和过去节点的属性和内容，将文本提取组合成文章。

所以程序可以分为两部分：

1. 给出遍历方式顺序的流程控制部分：深度优先遍历树
2. 根据规则进行提取并组合成文章

## 项目内容：

1. EEBO/OLL数据库网页，暂时用先下载html文件再处理的方式，使用浏览器插件 SingleFile
2. DeepL的自动翻译，使用DeepL提供的API接口，需要一个DeepL pro账号
3. 整理输出成txt，pkl，Word文件

## 处理来自EEBO的网页：

### 规律与规则：

1. 关于分段和分页
   
   ```html
   <br> <!-- 两个及以上的<br>或<hr>一起出现，有可能分段  -->
   <hr> <!-- <hr>是分页,  -->
   ```
   
   图片前后同样会出现它们
   
   判断是否分段：`<br>/<hr>`前的最后一个文本，是否以句号结尾，如果是，则分段

2. 特殊标记的词
   
   ```html
   <span>/<em>
   ```
   
   其中的内容是一个词或一组标签，如果下一个元素也是他们，则要加空格

3. 引用：
   
   ```html
   <div data-pqp-search-type="quotation">
       <blockquote>
   ```

4. 文本特征：
   
   所有的内容，前后都有引号，普通内容不用添加空格，span内容需要

5. Sec块的嵌套：
   
   EEBO数据库中，有一些文章会有Sec块`div[1-9]+ id="Sec[0-9]+"` 结构的嵌套，如：
   
   ```html
   <div1 id="Sec001">
     <!-- abaaba  -->
     <div2 id="Sec002">
         <div3 id="Sec003">
         <!-- abaaba  -->
   ```

### 需要跳过的不要的标签：

```html
<div class="document_view_dpmi_image">
<small>
```

## 处理来自OLL的网页

### 规律与规则：

1. 换行/段落：每个div/p都是一段
   
   ```html
   <div> </div>
   <p> </p>
   ```

2. 文章信息都在meta titlepage中
   
   ```html
   <div class="meta titlepage">
   ```

3. 文本都在每一节的`<p>`中：
   
   ```html
   <div id="lf[0-9]+_div_[0-9]+">
     <p>...</p>
   ```

4. 文本内容

## BUG：
