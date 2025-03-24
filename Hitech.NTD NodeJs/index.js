// import { sum,div,mul,sub } from "./math.js";
// console.log(sum(2,3));
// console.log(div(2,3));
// console.log(mul(2,3));
// console.log(sub(2,3));

// // thu vien tich hop san tinh toan
// import lodash from 'lodash';

// console.log(lodash.sum([1, 2, 3, 4, 5])); // 15
// console.log(lodash.partition([1, 2, 3, 4, 5], n => n % 2)); // [[1, 3, 5], [2, 4]]


// File System
// Read/Write file
// Folder access
// const fs = require('fs');
// const path = require('path');

// function readFile(filePath) {
// console.log('Reading file...');
// // doc file
// fs.readFile(filePath, 'utf8', (err, data) => {
//     if (err) {
//         console.error(err);
//         return;
//     }
//     console.log(data);
// });
// // ghi file
// fs.writeFile(filePath, "{id : 1 , name : 'cong ty hites'}", (err) => {
//     if (err) {
//         console.error(err);
//         return;
//     }
//     console.log('Writing file...');
// });
// // xoa file
// fs.unlink(filePath, (err) => {
//     if (err) {
//         console.error(err);
//         return;
//     }
//     console.log('Deleting file...');
// });
// }



// readFile(path.join(__dirname, 'file.txt'))


// Xử lý Buffer
// const buffer = Buffer.from('Hello, world!', 'utf8');
// console.log(buffer);  // <Buffer 48 65 6c 6c 6f 2c 20 77 6f 72 6c 64 21>
// // Chuyển buffer sang chuỗi
// console.log(buffer.toString());  // Hello, world!
// // chuyen buffer sang base64
// console.log(buffer.toString('base64'));  // SGVsbG8sIHdvcmxkIQ==
// // chuyen buffer sang hex
// console.log(buffer.toString('hex'));  // 48656c6c6f2c20776f726c6421
// // chuyen buffer sang json
// console.log(buffer.toJSON());  // { type: 'Buffer', data: [ 72, 101, 108, 108, 111, 44, 32, 119, 111, 114, 108, 100, 33 ] }
// // chuyen buffer sang utf8
// console.log(Buffer.from(buffer.toString('base64'), 'base64').toString('utf8'));  // Hello, world!

const fs = require('fs');
const path = require('path');


// function readFileCallback(filePath, callback) {
//     fs.readFile(filePath, 'utf8', (err, data) => {
//         if (err) {
//             callback(err, null);
//             return;
//         }
//         callback(null, data);
//     });
// }
//  Run time 1ms
// readFileCallback(path.join(__dirname, 'file.txt'), (err, data) => {
//     if (err) {
//         console.error('Lỗi khi đọc file:', err);
//     } else {
//         console.log('Nội dung file:', data);
//     }
// });


// function readFilePromise(filePath) {
//     return new Promise((resolve, reject
//     ) => {
//         fs.readFile(filePath, 'utf8', (err, data) => {
//             if (err) {
//                 reject(err);
//                 return;
//             }
//             resolve(data);
//         });
//     });
// }
// run time 0.9 ms < 1 ms
// readFilePromise(path.join(__dirname, 'file.txt'))
// .then(data => {
//     console.log('Nội dung file:', data);
// })
// .catch(err => {
//     console.error('Lỗi khi đọc file:', err);
// });

// clean async await
// async function readFileAsync(filePath) {
//     try {
//         const data = await readFilePromise(filePath);
//         console.log('Nội dung file:', data);
//     } catch (error) {
//         console.log('failed read file'); 
        
//     }
    
// }
// console.time('Start reading file...');

// readFileAsync(path.join(__dirname, 'file.txt'))
// console.timeEnd('Start reading file...');  0.8 ms < 1 ms

// function fakeApiCall(url) {
//     return new Promise((resolve, reject) => {
//         console.log(`Calling API: ${url}...`);
//         setTimeout(() => {
//             const success = Math.random() > 0.2
//             if (success) {
//                 resolve({ data: 'Data from API' });
//             } else {
//                 reject(new Error('Failed to call API'));
//             }
//         }, 2000);
        
//     })
// }
// fakeApiCall('https://fakestoreapi.com/products')
// .then(res => {
//     console.log(res);
// })
// .catch(err => {
//     console.error(err);
// });

// async function callApi(url) {
//     try {
//         const resposne = await fakeApiCall(url);
//         console.log(resposne);
        
//     } catch (error) {
//         console.log('Failed to call API' + error);
        
//     }
    
// }
// console.time();

// callApi('https://fakestoreapi.com/products')
// console.timeEnd(); // 4s - 2s production = 2s run time local

// import  http from 'http';
// Http module,status code and format
// const http = require('http');

// const app = http.createServer();

// app.on('request', (req, res) => {
//     res.writeHead(200, { 'Content-Type': 'text/plain' });
//     res.end('Hello, world!');
// });
// app.listen(3000, (req,res) => {
//     console.log('Server is running on port 3000');
// })
// ExpressJS framework
const express = require('express');

const app = express();
app.use(express.json());
// app.get('/', (req, res) => {
//     res.send('Hello, world!');
// });
// app.get('/about', (req, res) => {
//     res.send('About us');
// });

// app.get('/contact', (req, res) => {
//     res.send('Contact us');
// });
//  RESTful API
// const data = [
//     { id: 1, name: 'Product 1' },
//     { id: 2, name: 'Product 2' },
//     { id: 3, name: 'Product 3' },
// ]
// // get products
// app.get('/products/:id' , (req, res) => {
//     // res.json({ message: 'Hello, world!' });
//     try {
//         const id = req.params.id;
//         const product = data.find(item => item.id === Number(id));
//         if (product) {
//             res.json(product);
//         }
//     } catch (error) {
//         console.log('Failed to get product');
        
//     }
// });

// // create products
// app.post('/products', (req, res) => {
//     const product = req.body;
//     if (product) {
//         data.push(product);
//         console.log("Product created");
        
//         res.json(product);
//     }
 
// });
// // put products
// app.put('/products/:id', (req, res) => {
//     const id = req.params.id;
//     const product = data.find(item => item.id === Number(id));
//     if (product) {
//         product.name = req.body.name;       
//         res.json(product);
//     }
// });

// // delete products id
// app.delete('/products/:id', (req, res) => {
//     const id = req.params.id;
//     const productIndex = data.findIndex(item => item.id === Number(id));
//     if (productIndex !== -1) {
//         data.splice(productIndex, 1);
//         res.json({ message: 'Product deleted' });
//     }
// });

// // delete all products
// app.delete('/products', (req, res) => {
//     data.splice(0, data.length);
//     res.json({ message: 'All products deleted' });
// });


// Practice: task list management api
let tasks = []
// get all tasks
app.get('/tasks', (req, res) => {
    res.json(tasks);
});
// create task
app.post('/tasks', (req, res) => {
    const task = req.body;
    if (!task.title) {
        res.status(400).json({ message: 'Title is required' });
        return;
    }
     if (task) {
        let id = tasks.length + 1;

        tasks.push({
            id,
            ...task,
            completed: false
        });
        res.json(task);
    }
});

// update task
app.put('/tasks/:id', (req, res) => {
    const id = req.params.id;
    const task = tasks.find(item => item.id === Number(id));
    if (task) {
        task.title = req.body.title;
        task.completed = req.body.completed;
        res.json(task);
    }
}); 

// delete task
app.delete('/tasks/:id', (req, res) => {
    const id = req.params.id;
    const taskIndex = tasks.findIndex(item => item.id === Number(id));
    if (taskIndex !== -1) {
        tasks.splice(taskIndex, 1);
        res.json({ message: 'Task deleted' });
    }
});

// Create a db mongo
// vidu :
/**
 * usermodel : {
 * id : {type : Number, required : true, unique : true},
 * title : {type : String, required : true},
 * des : {type : String , default : ''},
 * completed : {type : Boolean , default : false}
 * }
 * 
 * // create user insert db
 * let id =  usermodel.length + 1;
 * const user = new UserModel.create({title : 'task 1', des : 'task 1 des', completed : false});
 *
 * // update user
 * UserModel.updateOne({id : 1}, {title : 'task 2', des : 'task 2 des', completed : true});
 * 
 * // delete user
 * UserModel.deleteOne({id : 1});
 * 
 * // get user
 * UserModel.find({id : 1}); 
 */
// const task = ai
app.listen(3000, () => {
    console.log('Server is running on port 3000');
})