package ec.xpd.apcisnomina.entidades;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import javax.persistence.Column;
import java.util.Date;

@Entity
@Table(name="employees")
@JsonIgnoreProperties("hibernateLazyInitializer")
public class Employee {
	@Id
	@GeneratedValue(strategy =  GenerationType.IDENTITY)
	@Column(name = "id")
	private Integer id;
	
	@Column(name = "created_by")
	private String createdBy;
	
	@Column(name = "created_date")
	private Date createdDate;
	
	@Column(name = "modified_by")
	private String modifiedBy;
	
	@Column(name = "modified_date")
	private Date modifiedDate;
	
	@Column(name = "status")
	private Boolean status;
	
	@Column(name = "age")
	private int age;
	
	@Column(name = "email")
	private String email;
	
	@Column(name = "name")
	private String name;
	
	@Column(name = "position")
	private String position;
	
	@Column(name = "surname")
	private String surname;

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getCreatedBy() {
		return createdBy;
	}

	public void setCreatedBy(String createdBy) {
		this.createdBy = createdBy;
	}

	public Date getCreatedDate() {
		return createdDate;
	}

	public void setCreatedDate(Date createdDate) {
		this.createdDate = createdDate;
	}

	public String getModifiedBy() {
		return modifiedBy;
	}

	public void setModifiedBy(String modifiedBy) {
		this.modifiedBy = modifiedBy;
	}

	public Date getModifiedDate() {
		return modifiedDate;
	}

	public void setModifiedDate(Date modifiedDate) {
		this.modifiedDate = modifiedDate;
	}

	public Boolean getStatus() {
		return status;
	}

	public void setStatus(Boolean status) {
		this.status = status;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getPosition() {
		return position;
	}

	public void setPosition(String position) {
		this.position = position;
	}

	public String getSurname() {
		return surname;
	}

	public void setSurname(String surname) {
		this.surname = surname;
	}
	
}
