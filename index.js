import React, { Component } from "react";
import { Button, Glyphicon } from "react-bootstrap";
import TaskTabs from "./TaskTabs";
import "./index.scss";

export default class TaskList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      tasks: [],
      activeTab: 0,
      taskCreation: false,
      editorOpen: false
    };
  }

  handleTaskCreateButtonPress(type) {
    this.setState({
      taskCreation: type
    });
  }

  handleTaskCreationClose() {
    this.setState({
      taskCreation: false,
      editorOpen: false
    });
  }

  handleTabPress(tab) {
    this.setState({
      activeTab: tab
    });
  }

  handleTaskSubmission(task) {
    let taskListRef = this.props.database.ref().child('taskList');
    let taskKey = task.taskID ? task.taskID : taskListRef.push().key;
    task.taskID = taskKey;
    task.taskDate = new Date(task.taskDate).getTime();
    let updates = {};
    updates[taskKey] = task;
    taskListRef.update(updates);
    this.setState({
      taskCreation: false
    });
  }

  handleTaskCompleted(task) {
      let taskAssignee = task.assignedTo
      if (taskAssignee === undefined) {
        let taskKey = task.taskID;
        task.isComplete = !task.isComplete;
        task.taskDate = new Date(task.taskDate).getTime();
        let updates = {};
        updates['/taskList/' + taskKey] = task;
        this.props.database.ref().update(updates);
      }
      else {
        for (let i = 0; i <= (taskAssignee.length); i++) {
          if (this.props.user.uid === taskAssignee[i]) {
            let taskKey = task.taskID;
            task.isComplete = !task.isComplete;
            task.taskDate = new Date(task.taskDate).getTime();
            let updates = {};
            updates['/taskList/' + taskKey] = task;
            this.props.database.ref().update(updates);
          }
        }
      }
  }

  handleDeleteTask(task) {
    let taskKey = task.taskID;
    task.isDeleted = 1;
    task.taskDate = new Date(task.taskDate).getTime();
    let updates = {};
    updates['/taskList/' + taskKey] = task;
    this.props.database.ref().update(updates);
  }

  render() {
    let createTaskButtons = (
      <div>
        <Button
          id="addChoreButton"
          onClick={() => this.handleTaskCreateButtonPress("Chore")}
        >
          <Glyphicon glyph="plus" /> Chore
        </Button>
        <Button
          id="addPurchaseButton"
          onClick={() => this.handleTaskCreateButtonPress("Purchase")}
        >
          <Glyphicon glyph="plus" /> Purchase
        </Button>
      </div>
    );

    let task_tabs = (
      <TaskTabs
        task = {this.props.task}
        user={this.props.user}
        tasks={this.state.tasks}
        database={this.props.database}
        groupID={this.props.groupID}
        personsInGroup={this.props.personsInGroup}
        activeTab={this.state.activeTab}
        taskCreation={this.state.taskCreation}
        handleTabPress={t => this.handleTabPress(t)}
        handleTaskSubmission={task => this.handleTaskSubmission(task)}
        handleTaskCompleted={task => this.handleTaskCompleted(task)}
        handleDeleteTask={t => this.handleDeleteTask(t)}
        handleTaskCreationClose={() => this.handleTaskCreationClose()}
      />
    );

    const tasklist = (
      <div>
        <div className="TaskList">
          <h1>Task List</h1>
          {createTaskButtons}
          {task_tabs}
        </div>
      </div>
    );

    let pageToReturn = tasklist;

    return pageToReturn;
  }
}
