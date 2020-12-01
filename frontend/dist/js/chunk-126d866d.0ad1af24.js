(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-126d866d"],{1813:function(t,e,r){"use strict";var n=r("d4ec"),o=r("bee2"),i=r("c427"),a=function(){function t(){Object(n["a"])(this,t)}return Object(o["a"])(t,[{key:"getAll",value:function(){return i["a"].get("patients/")}},{key:"getAllByDoctor",value:function(t){return i["a"].get("patients/",{params:{main_doctor:t}})}},{key:"get",value:function(t){return i["a"].get("patients/".concat(t))}},{key:"create",value:function(t){return i["a"].post("patients/",t)}},{key:"update",value:function(t,e){return i["a"].put("patients/".concat(t,"/"),e)}},{key:"delete",value:function(t){return i["a"].delete("patients/".concat(t))}},{key:"deleteAll",value:function(){return i["a"].delete("patients")}}]),t}();e["a"]=new a},"184d":function(t,e,r){"use strict";var n=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",[r("vs-table",{staticClass:"patients__table",attrs:{striped:""},scopedSlots:t._u([{key:"header",fn:function(){return[r("vs-input",{attrs:{border:"",placeholder:"Search"},model:{value:t.searchValue,callback:function(e){t.searchValue=e},expression:"searchValue"}})]},proxy:!0},{key:"thead",fn:function(){return[r("vs-tr",[r("vs-th",[t._v(" Name ")]),r("vs-th",[t._v(" Date of birth ")]),r("vs-th",[t._v(" Email contact ")]),r("vs-th",[t._v(" Gender ")])],1)]},proxy:!0},{key:"tbody",fn:function(){return t._l(t.$vs.getPage(t.$vs.getSearch(t.patients,t.searchValue),t.page,t.max),(function(e,n){return r("vs-tr",{key:n,attrs:{data:e}},[r("vs-td",[r("span",{staticClass:"redirect__profile",on:{click:function(r){return t.redirectToPatientProfile(e.user.id,"patient")}}},[r("b",[t._v(t._s(e.user.first_name)+" "+t._s(e.user.last_name))])])]),r("vs-td",[t._v(" "+t._s(t.getDate(e.user.date_of_birth))+" ")]),r("vs-td",[t._v(" "+t._s(e.user.email)+" ")]),r("vs-td",[t._v(" "+t._s(t.getGender(e.user.gender))+" ")])],1)}))},proxy:!0},{key:"footer",fn:function(){return[r("vs-pagination",{attrs:{length:t.$vs.getLength(t.patients,t.max)},model:{value:t.page,callback:function(e){t.page=e},expression:"page"}})]},proxy:!0}])})],1)},o=[],i=(r("ac1f"),r("5319"),r("fa1c")),a={name:"PatientsTable",props:{patients:{}},data:function(){return{page:1,max:10,searchValue:""}},methods:{redirectToPatientProfile:function(t,e){this.$router.push({name:"profile",params:{id:t,role:e.replace(/ /g,"-").toLowerCase()}}),"/patients"!==this.$route.path&&this.$router.go()},getDate:function(t){return i["a"].getDateForFrontend(t)},getGender:function(t){return"M"===t?"Male":"F"===t?"Female":"O"===t?"Other":void 0}}},c=a,u=(r("75e2"),r("0c7c")),s=Object(u["a"])(c,n,o,!1,null,"71fa2e62",null);e["a"]=s.exports},"1da1":function(t,e,r){"use strict";r.d(e,"a",(function(){return o}));r("d3b7");function n(t,e,r,n,o,i,a){try{var c=t[i](a),u=c.value}catch(s){return void r(s)}c.done?e(u):Promise.resolve(u).then(n,o)}function o(t){return function(){var e=this,r=arguments;return new Promise((function(o,i){var a=t.apply(e,r);function c(t){n(a,o,i,c,u,"next",t)}function u(t){n(a,o,i,c,u,"throw",t)}c(void 0)}))}}},"20cf":function(t,e,r){},"75e2":function(t,e,r){"use strict";var n=r("20cf"),o=r.n(n);o.a},"96cf":function(t,e,r){var n=function(t){"use strict";var e,r=Object.prototype,n=r.hasOwnProperty,o="function"===typeof Symbol?Symbol:{},i=o.iterator||"@@iterator",a=o.asyncIterator||"@@asyncIterator",c=o.toStringTag||"@@toStringTag";function u(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{u({},"")}catch(A){u=function(t,e,r){return t[e]=r}}function s(t,e,r,n){var o=e&&e.prototype instanceof y?e:y,i=Object.create(o.prototype),a=new F(n||[]);return i._invoke=E(t,r,a),i}function l(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(A){return{type:"throw",arg:A}}}t.wrap=s;var f="suspendedStart",h="suspendedYield",p="executing",v="completed",d={};function y(){}function g(){}function m(){}var w={};w[i]=function(){return this};var b=Object.getPrototypeOf,_=b&&b(b(S([])));_&&_!==r&&n.call(_,i)&&(w=_);var x=m.prototype=y.prototype=Object.create(w);function k(t){["next","throw","return"].forEach((function(e){u(t,e,(function(t){return this._invoke(e,t)}))}))}function L(t,e){function r(o,i,a,c){var u=l(t[o],t,i);if("throw"!==u.type){var s=u.arg,f=s.value;return f&&"object"===typeof f&&n.call(f,"__await")?e.resolve(f.__await).then((function(t){r("next",t,a,c)}),(function(t){r("throw",t,a,c)})):e.resolve(f).then((function(t){s.value=t,a(s)}),(function(t){return r("throw",t,a,c)}))}c(u.arg)}var o;function i(t,n){function i(){return new e((function(e,o){r(t,n,e,o)}))}return o=o?o.then(i,i):i()}this._invoke=i}function E(t,e,r){var n=f;return function(o,i){if(n===p)throw new Error("Generator is already running");if(n===v){if("throw"===o)throw i;return G()}r.method=o,r.arg=i;while(1){var a=r.delegate;if(a){var c=O(a,r);if(c){if(c===d)continue;return c}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if(n===f)throw n=v,r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n=p;var u=l(t,e,r);if("normal"===u.type){if(n=r.done?v:h,u.arg===d)continue;return{value:u.arg,done:r.done}}"throw"===u.type&&(n=v,r.method="throw",r.arg=u.arg)}}}function O(t,r){var n=t.iterator[r.method];if(n===e){if(r.delegate=null,"throw"===r.method){if(t.iterator["return"]&&(r.method="return",r.arg=e,O(t,r),"throw"===r.method))return d;r.method="throw",r.arg=new TypeError("The iterator does not provide a 'throw' method")}return d}var o=l(n,t.iterator,r.arg);if("throw"===o.type)return r.method="throw",r.arg=o.arg,r.delegate=null,d;var i=o.arg;return i?i.done?(r[t.resultName]=i.value,r.next=t.nextLoc,"return"!==r.method&&(r.method="next",r.arg=e),r.delegate=null,d):i:(r.method="throw",r.arg=new TypeError("iterator result is not an object"),r.delegate=null,d)}function j(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function P(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function F(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(j,this),this.reset(!0)}function S(t){if(t){var r=t[i];if(r)return r.call(t);if("function"===typeof t.next)return t;if(!isNaN(t.length)){var o=-1,a=function r(){while(++o<t.length)if(n.call(t,o))return r.value=t[o],r.done=!1,r;return r.value=e,r.done=!0,r};return a.next=a}}return{next:G}}function G(){return{value:e,done:!0}}return g.prototype=x.constructor=m,m.constructor=g,g.displayName=u(m,c,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"===typeof t&&t.constructor;return!!e&&(e===g||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,m):(t.__proto__=m,u(t,c,"GeneratorFunction")),t.prototype=Object.create(x),t},t.awrap=function(t){return{__await:t}},k(L.prototype),L.prototype[a]=function(){return this},t.AsyncIterator=L,t.async=function(e,r,n,o,i){void 0===i&&(i=Promise);var a=new L(s(e,r,n,o),i);return t.isGeneratorFunction(r)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},k(x),u(x,c,"Generator"),x[i]=function(){return this},x.toString=function(){return"[object Generator]"},t.keys=function(t){var e=[];for(var r in t)e.push(r);return e.reverse(),function r(){while(e.length){var n=e.pop();if(n in t)return r.value=n,r.done=!1,r}return r.done=!0,r}},t.values=S,F.prototype={constructor:F,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=e,this.done=!1,this.delegate=null,this.method="next",this.arg=e,this.tryEntries.forEach(P),!t)for(var r in this)"t"===r.charAt(0)&&n.call(this,r)&&!isNaN(+r.slice(1))&&(this[r]=e)},stop:function(){this.done=!0;var t=this.tryEntries[0],e=t.completion;if("throw"===e.type)throw e.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var r=this;function o(n,o){return c.type="throw",c.arg=t,r.next=n,o&&(r.method="next",r.arg=e),!!o}for(var i=this.tryEntries.length-1;i>=0;--i){var a=this.tryEntries[i],c=a.completion;if("root"===a.tryLoc)return o("end");if(a.tryLoc<=this.prev){var u=n.call(a,"catchLoc"),s=n.call(a,"finallyLoc");if(u&&s){if(this.prev<a.catchLoc)return o(a.catchLoc,!0);if(this.prev<a.finallyLoc)return o(a.finallyLoc)}else if(u){if(this.prev<a.catchLoc)return o(a.catchLoc,!0)}else{if(!s)throw new Error("try statement without catch or finally");if(this.prev<a.finallyLoc)return o(a.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var o=this.tryEntries[r];if(o.tryLoc<=this.prev&&n.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var i=o;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=e&&e<=i.finallyLoc&&(i=null);var a=i?i.completion:{};return a.type=t,a.arg=e,i?(this.method="next",this.next=i.finallyLoc,d):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),d},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),P(r),d}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var o=n.arg;P(r)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(t,r,n){return this.delegate={iterator:S(t),resultName:r,nextLoc:n},"next"===this.method&&(this.arg=e),d}},t}(t.exports);try{regeneratorRuntime=n}catch(o){Function("r","regeneratorRuntime = r")(n)}},bee2:function(t,e,r){"use strict";function n(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}function o(t,e,r){return e&&n(t.prototype,e),r&&n(t,r),t}r.d(e,"a",(function(){return o}))},d4ec:function(t,e,r){"use strict";function n(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}r.d(e,"a",(function(){return n}))},fa1c:function(t,e,r){"use strict";r("fb6a");var n=r("d4ec"),o=r("bee2"),i=function(){function t(){Object(n["a"])(this,t)}return Object(o["a"])(t,[{key:"getDateForBackend",value:function(t){var e=t.slice(8,10),r=t.slice(5,7),n=t.slice(0,4);return n+"-"+r+"-"+e}},{key:"getDateForFrontend",value:function(t){var e=t.slice(0,4),r=t.slice(5,7),n=t.slice(8,10),o=t.slice(11,19);return n+". "+r+". "+e+" "+o}}]),t}();e["a"]=new i},fb6a:function(t,e,r){"use strict";var n=r("23e7"),o=r("861d"),i=r("e8b5"),a=r("23cb"),c=r("50c4"),u=r("fc6a"),s=r("8418"),l=r("b622"),f=r("1dde"),h=r("ae40"),p=f("slice"),v=h("slice",{ACCESSORS:!0,0:0,1:2}),d=l("species"),y=[].slice,g=Math.max;n({target:"Array",proto:!0,forced:!p||!v},{slice:function(t,e){var r,n,l,f=u(this),h=c(f.length),p=a(t,h),v=a(void 0===e?h:e,h);if(i(f)&&(r=f.constructor,"function"!=typeof r||r!==Array&&!i(r.prototype)?o(r)&&(r=r[d],null===r&&(r=void 0)):r=void 0,r===Array||void 0===r))return y.call(f,p,v);for(n=new(void 0===r?Array:r)(g(v-p,0)),l=0;p<v;p++,l++)p in f&&s(n,l,f[p]);return n.length=l,n}})}}]);
//# sourceMappingURL=chunk-126d866d.0ad1af24.js.map