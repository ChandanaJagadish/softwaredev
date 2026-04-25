const express = require('express');
const cors = require('cors');
const sequelize = require('./db');
require('dotenv').config();

require('./models/User');
require('./models/Task');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('../frontend'));

app.use('/api/auth', require('./routes/auth'));
app.use('/api/tasks', require('./routes/tasks'));

sequelize.sync({ alter: true })
  .then(() => {
    console.log('✅ PostgreSQL connected & tables ready');
    app.listen(process.env.PORT, () =>
      console.log(`✅ Server running at http://localhost:${process.env.PORT}`)
    );
  })
  .catch(err => console.log('❌ DB error:', err));