package ec.xpd.apcisnomina.entidades;

import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import javax.persistence.Column;
import java.util.Date;

@Entity
@Table(name="departments_employees")
@JsonIgnoreProperties("hibernateLazyInitializer")
public class DepartmentEmployee {
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

	@Column(name = "id_department")
	private int idDepartment;
	
	@Column(name = "id_employee")
	private int idEmployee;

	@ManyToOne( fetch = FetchType.LAZY )
	@JoinColumn( name="id_department"  , insertable=false, updatable=false)
	private Department department;
	
	@ManyToOne( fetch = FetchType.LAZY )
	@JoinColumn( name="id_employee"  , insertable=false, updatable=false)
	private Employee employee;

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

	public Department getDepartment() {
		return department;
	}

	public void setDepartment(Department department) {
		this.department = department;
	}

	public Employee getEmployee() {
		return employee;
	}

	public void setEmployee(Employee employee) {
		this.employee = employee;
	}

	public int getIdDepartment() {
		return idDepartment;
	}

	public void setIdDepartment(int idDepartment) {
		this.idDepartment = idDepartment;
	}

	public int getIdEmployee() {
		return idEmployee;
	}

	public void setIdEmployee(int idEmployee) {
		this.idEmployee = idEmployee;
	}
}
