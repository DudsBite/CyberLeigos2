const vm=require('vm'),fs=require('fs');
module.exports=function(files){const sb={};sb.window=sb;vm.createContext(sb);for(const f of files)vm.runInContext(fs.readFileSync(f,'utf8'),sb,{filename:f});return sb.CL;};
