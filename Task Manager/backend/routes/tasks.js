const router = require('express').Router();
const jwt = require('jsonwebtoken');
const Task = require('../models/Task');

const auth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ msg: 'No token' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ msg: 'Invalid token' });
  }
};

router.get('/', auth, async (req, res) => {
  const tasks = await Task.findAll({
    where: { userId: req.user.id },
    order: [['createdAt', 'DESC']]
  });
  res.json(tasks);
});

router.post('/', auth, async (req, res) => {
  const task = await Task.create({
    title: req.body.title,
    userId: req.user.id
  });
  res.json(task);
});

router.put('/:id', auth, async (req, res) => {
  await Task.update(req.body, { where: { id: req.params.id, userId: req.user.id } });
  const task = await Task.findByPk(req.params.id);
  res.json(task);
});

router.delete('/:id', auth, async (req, res) => {
  await Task.destroy({ where: { id: req.params.id, userId: req.user.id } });
  res.json({ msg: 'Deleted' });
});

module.exports = router;